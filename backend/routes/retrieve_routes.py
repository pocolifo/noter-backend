from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *
from dependency import auth_dependency

db = DB(CONN_LINK())
db.connect()

router = APIRouter()

@router.get("/items/{id}")
async def get_item(request: Request, id: str, is_auth: bool = Depends(auth_dependency)):
    item = db.get_item(request, id)
    if not item: return Response(status_code=404)
    return JSONResponse(json.loads(item), status_code=200)
    
    
@router.post("/items/list")
async def list_items(request: Request, is_auth: bool = Depends(auth_dependency)):
    ret = []
    
    try: path = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, path): return Response(status_code=400)
            
    curr_users_notes = db.note_manager.get_users_notes(request)
    for n in curr_users_notes:               
        if str(n["path"]) == str(path): ret.append(n)
            
    curr_users_folders = db.folder_manager.get_users_folders(request)
    for f in curr_users_folders:
        if str(f["path"]) == str(path): ret.append(f)
        
    return JSONResponse(status_code=200, content=ret)
    