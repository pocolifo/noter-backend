import json, os, redis

from fastapi import HTTPException
from starlette.requests import Request
from typing import Union

from backend.noterdb import DB, db
from backend.utils import from_jwt

rdb = redis.Redis(
    host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'],
    username=os.environ['REDIS_USER'],
    password=os.environ['REDIS_PASS'], decode_responses=True)

async def auth_dependency(request: Request) -> Union[bool, dict]:
    user_id = from_jwt(str(request.cookies.get("authenticate")))
    
    if not db.is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not Authenticated")
    
    return json.loads(db.user_manager.get_user_data_by_id(user_id))
    
async def global_checks(request: Request):
    global_api_access = bool(int(rdb.get("global_api_access")))
    ai_endpoints = bool(int(rdb.get("ai_endpoints")))
    item_creation = bool(int(rdb.get("item_creation")))
    user_creation = bool(int(rdb.get("user_creation")))
    
    if not global_api_access: raise HTTPException(status_code=503, detail="Service Unavailable")
    if request.url.path.startswith("/ai") and not ai_endpoints: raise HTTPException(status_code=503, detail="Service Unavailable")
    
    if request.url.path.startswith("/items/create/user"):
        if not user_creation: raise HTTPException(status_code=503, detail="Service Unavailable")
        else: return
    
    if request.url.path.startswith("/items/create") and not item_creation: raise HTTPException(status_code=503, detail="Service Unavailable")
    return