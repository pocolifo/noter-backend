import json

from fastapi import HTTPException
from starlette.requests import Request
from typing import Union

from backend.noterdb import DB
from backend.globals import CONN_LINK
from backend.utils import from_jwt


db = DB(CONN_LINK())
db.connect()

async def auth_dependency(request: Request) -> Union[bool, dict]:
    user_id = from_jwt(str(request.cookies.get("authenticate")))
    
    if not db.is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    return json.loads(db.user_manager.get_user_data_by_id(user_id))