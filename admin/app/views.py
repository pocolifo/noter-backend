from datetime import datetime
import hashlib
import os
from typing import Any, Coroutine
import httpx
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin.views import CustomView
from sqlalchemy.engine import Engine
from sqlalchemy import select, func

from backend.tables import User, Note, Folder

class HomeView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:
        users_registered = request.state.session.query(func.count(User.id)).scalar()
        users_with_access = request.state.session.query(func.count(User.has_noter_access == True)).scalar()
        notes_created = request.state.session.query(func.count(Note.id)).scalar()
        folders_created = request.state.session.query(func.count(Folder.id)).scalar()

        return templates.TemplateResponse(
            'HomeView.html.j2',
            {
                'request': request,
                'stats': [
                    {
                        'name': 'users registered',
                        'value': users_registered
                    },
                    {
                        'name': 'users with Noter access',
                        'value': users_with_access
                    },
                    {
                        'name': 'notes created',
                        'value': notes_created
                    },
                    {
                        'name': 'folders created',
                        'value': folders_created
                    }
                ]
            }
        )


class AccessFlagsView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{os.environ['META_SERVER_URL']}/access-flags")
            flags = response.json()
            update_success = None

            if request.method == 'POST':
                data = await request.form(max_files=0, max_fields=len(flags) + 1)  # +1 for authorization secret field
                secret = data.get('authorization-secret')
                
                for flag, _ in flags.items():
                    flags[flag] = False

                for flag, _ in data.items():
                    if not flag.startswith('flag__'):
                        continue

                    flag = flag.removeprefix('flag__')
                    flags[flag] = True
                
                # Key algorithm as specified in the meta project
                now = datetime.now()
                salt = hashlib.sha512(f'{now.year}{now.month}{now.day}{now.hour}{now.minute}'.encode('utf-8')).hexdigest()
                expected_string = f'{secret}{salt}'

                update_request = httpx.put(f"{os.environ['META_SERVER_URL']}/access-flags", json=flags, headers={
                    'Authorization': expected_string
                })

                update_success = 200 <= update_request.status_code <= 299

            return templates.TemplateResponse(
                'AccessFlags.html.j2', { 'request': request, 'flags': flags, 'update': update_success }
            )