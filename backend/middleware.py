from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *

db = DB(CONN_LINK())
db.connect()

no_auth = ["/", "/authenticate", "/items/create/user", ]
async def route_middleware(request: Request, call_next):
    if str(request.url.path) not in no_auth:
        if not db.is_authenticated(request): return Response(status_code=401)
    
    
    response = await call_next(request)
    return response


























