from backend.environment import load_all, append_to_environ
append_to_environ(load_all())

import json
import os
import stripe

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from pydantic import BaseModel

from backend.noterdb import db
from backend.utils import verify_hash, to_jwt, get_current_isodate, from_jwt, clean_udata
from backend.dependency import require_access_flag
from backend.models.requests import UserCredentialsRequest

import backend.routes.retrieve_routes as rr
import backend.routes.update_routes as ur
import backend.routes.create_routes as cr
import backend.routes.account_routes as ac
import backend.routes.stripe_webhook_routes as swr
import backend.gptroutes.ai_routes as air

# OpenAI API key is automatically set ot the OPENAI_API_KEY environment variable
stripe.api_key = os.environ['STRIPE_API_KEY']  # require it

app = FastAPI(title='Noter API', description='Backend API for Noter', dependencies=[Depends(global_checks)])

app.add_middleware(CORSMiddleware, allow_origins=os.environ['CORS_ALLOW_ORIGINS'].split(','), allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

app.include_router(rr.router)
app.include_router(ur.router)
app.include_router(cr.router)
app.include_router(ac.router)
app.include_router(swr.router)
app.include_router(air.router)


@app.middleware('http')
async def require_global_api_access(request: Request, call_next):
    require_access_flag('api_enabled')
    return await call_next(request)


@app.post("/authenticate")
async def authenticate(data: UserCredentialsRequest):
    u = db.user_manager.get_user_by_email(data.email)

    if not u:
        return {"authenticated": False}
    
    if u["email"] == data.email and verify_hash(u["password"], data.password):
        response = JSONResponse(status_code=200, content={"authenticated": True})
        
        response.set_cookie(key="authenticate", value=to_jwt(str(u["id"])), path="/")
        db.user_manager.update_column(str(u["id"]), "last_signed_in", str(get_current_isodate()))
        return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not db.is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": 1.1, "user":None})
        
    udata = clean_udata(json.loads(db.user_manager.get_user_data_by_id(from_jwt(str(request.cookies.get("authenticate"))))))
    
    return JSONResponse(status_code=200, content=(udata)) # add API version to response content


