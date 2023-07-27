import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from pydantic import BaseModel

from backend.globals import CONN_LINK, SMTP_LOGIN, CORS_ALLOW_ORIGINS, API_VERSION
from backend.noterdb import DB
from backend.smtputil import Client
from backend.utils import verify_hash, to_jwt, get_current_isodate, from_jwt

import backend.routes.retrieve_routes as rr
import backend.routes.update_routes as ur
import backend.routes.create_routes as cr
import backend.routes.account_routes as ac
import backend.routes.stripe_webhook_routes as swr
import backend.gptroutes.ai_routes as air

db = None
smtp_client = None
def app_init():
    global db, smtp_client
    db = DB(CONN_LINK())
    db.connect()
    
    smtp_login = SMTP_LOGIN()
    smtp_client = Client(smtp_login.get("server"), smtp_login.get("port"), smtp_login.get("email"), smtp_login.get("password"))
    smtp_client.connect()
    return FastAPI()

app = app_init()

app.add_middleware(CORSMiddleware, allow_origins=CORS_ALLOW_ORIGINS(), allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

app.include_router(rr.router)
app.include_router(ur.router)
app.include_router(cr.router)
app.include_router(ac.router)
app.include_router(swr.router)
app.include_router(air.router)


class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(request: Request, data: AuthData):
    u = db.user_manager.get_user_by_email(data.email)
    if u is None: return {"authenticated": False}
    
    if u["email"] == data.email and verify_hash(u["password"], data.password):
        response = JSONResponse(status_code=200, content={"authenticated": True})
        
        response.set_cookie(key="authenticate", value=to_jwt(str(u["id"])), path="/")
        db.user_manager.update_column(str(u["id"]), "last_signed_in", str(get_current_isodate()))
        return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not db.is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION(), "user":None})
        
    udata = json.loads(db.user_manager.get_user_data_by_id(from_jwt(str(request.cookies.get("authenticate")))))
    udata.pop("password")
    return JSONResponse(status_code=200, content=(udata)) # add API version to response content

