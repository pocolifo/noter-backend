import json, os
import httpx

from fastapi import HTTPException
from starlette.requests import Request
from typing import Union

from backend.noterdb import DB, db
from backend.utils import from_jwt


async def auth_dependency(request: Request) -> Union[bool, dict]:
    user_id = from_jwt(str(request.cookies.get("authenticate")))
    
    if not db.is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    return json.loads(db.user_manager.get_user_data_by_id(user_id))

async def require_access_flag(flag: str):
    # If in testing environment, just skip this because the meta server isn't run in test
    if 'PYTEST_CURRENT_TEST' in os.environ:
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(f'{os.environ["META_SERVER_URL"]}/access-flags')
        flags = response.json()

        if not flags[flag]:
            raise HTTPException(status_code=503, detail='Service Unavailable')

# TODO: better way to do this instead of having one function per access flag
# TODO: better names
async def require_api_access():
    await require_access_flag('api_enabled')

async def require_ai_access():
    await require_access_flag('ai_endpoints_enabled')

async def require_user_creation_access():
    await require_access_flag('user_creation_endabled')

async def require_item_creation_access():
    await require_access_flag('item_creation_enabled')