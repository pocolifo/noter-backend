from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from typing import Union

from noterdb import *
from globals import *

db = DB(CONN_LINK())
db.connect()

async def auth_dependency(request: Request) -> Union[bool, dict]:
    user_id = from_jwt(str(request.cookies.get("authenticate")))
    
    if not db.is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not Authenticated")
        return False
    
    return json.loads(db.user_manager.get_user_data_by_id(user_id))