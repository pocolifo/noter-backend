import uvicorn, json
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from make_objects import *
from utils import *
from globals import *
from noterdb import DB

import retrieve_routes as rr
import update_routes as ur
import create_routes as cr

db = None
def app_init():
    global db
    db = DB(CONN_LINK())
    db.connect()
    return FastAPI()

app = app_init()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'], allow_credentials=True)

app.include_router(rr.router)
app.include_router(ur.router)
app.include_router(cr.router)


@app.delete("/items/delete")
async def delete_item(request: Request, id: str):
    if not db.is_authenticated(request): return Response(status_code=401)

    db.delete_item_by_id(request, id)
    return Response(status_code=204)
        
    #return Response(status_code=400)


class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(request: Request, data: AuthData):
    pusers = db.user_manager.get_users_by_email(data.email)
    for u in pusers:
        print(u["password"])
        if u["email"] == data.email and verify_hash(u["password"], data.password):
            u["lastSignedIn"] = get_current_isodate() # UPDATE IN DB
            response = JSONResponse(status_code=200, content={"authenticated": True})
            response.set_cookie(key="authenticate", value=str(u["id"]), path="/")
            db.user_manager.update_lastsignedin(request)
            return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not db.is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION(), "user":0})
        
    udata = db.user_manager.get_user_data_by_id(request.cookies.get("authenticate"))
    return JSONResponse(status_code=200, content=udata) # add API version to response content


