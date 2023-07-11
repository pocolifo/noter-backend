from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import Response
from pydantic import BaseModel

from make_objects import *
from utils import *
from globals import *
from noterdb import DB
from middleware import route_middleware

import retrieve_routes as rr
import update_routes as ur
import create_routes as cr

db = None
def app_init():
    global db
    db = DB(CONN_LINK())
    db.connect()
    return FastAPI()

limiter = Limiter(key_func=get_remote_address)
app = app_init()

app.add_middleware(CORSMiddleware, allow_origins=CORS_ALLOW_ORIGINS(), allow_methods=['*'], allow_headers=['*'], allow_credentials=True)
app.middleware("http")(route_middleware)

app.include_router(rr.router)
app.include_router(ur.router)
app.include_router(cr.router)


@app.delete("/items/delete")
async def delete_item(request: Request, id: str):
    if not db.is_authenticated(request): return Response(status_code=401)

    db.delete_item_by_id(request, id)
    return Response(status_code=204)
        
    #return Response(status_code=400)

@limiter.limit("3/hour")
@app.post("/resend-verification")
async def resend_verification_email(request: Request):
    return Response(status_code=204)



class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(request: Request, data: AuthData):
    pusers = db.user_manager.get_users_by_email(data.email)
    for u in pusers:
        if u["email"] == data.email and verify_hash(u["password"], data.password):
            response = JSONResponse(status_code=200, content={"authenticated": True})
            
            response.set_cookie(key="authenticate", value=to_jwt(str(u["id"])), path="/")
            db.user_manager.update_lastsignedin(str(u["id"]))
            return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not db.is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION(), "user":None})
        
    udata = db.user_manager.get_user_data_by_id(from_jwt(str(request.cookies.get("authenticate"))))
    return JSONResponse(status_code=200, content=udata) # add API version to response content


