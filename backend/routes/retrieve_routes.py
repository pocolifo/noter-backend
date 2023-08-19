import json
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from backend.noterdb import DB, db
from backend.dependency import auth_dependency

router = APIRouter()

@router.get("/items/{id}")
async def get_item(request: Request, id: str, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    item = db.get_item(request, id)
    if not item: return Response(status_code=404)
    return JSONResponse(json.loads(item), status_code=200)
    
    
@router.post("/items/list")
async def list_items(request: Request, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    ret = []
    
    try: path = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, path): return Response(status_code=400)
            
    curr_users_notes = db.user_manager.get_notes(request)
    for n in curr_users_notes:               
        if str(n["path"]) == str(path): ret.append(n)
            
    curr_users_folders = db.user_manager.get_folders(request)
    for f in curr_users_folders:
        if str(f["path"]) == str(path): ret.append(f)
        
    return JSONResponse(status_code=200, content=ret)
    