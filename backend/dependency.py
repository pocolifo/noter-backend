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
    response = await httpx.get(f'{os.environ["META_SERVER"]}/access-flags')
    flags = await response.json()

    if not flags[flag]:
        raise HTTPException(status_code=503, detail='Service Unavailable')
