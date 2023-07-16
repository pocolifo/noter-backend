from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *

db = DB(CONN_LINK())
db.connect()

async def auth_dependency(request: Request):
    if not db.is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not Authenticated")
        return False
    
    return True