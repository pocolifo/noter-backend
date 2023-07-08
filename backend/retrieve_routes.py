from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *

db = DB(CONN_LINK())
db.connect()

router = APIRouter()

@router.get("/items/{id}")
async def get_item(request: Request, id: str):
    if not db.is_authenticated(request): return Response(status_code=401)

    item = db.get_item(request, id)
    if not item: return Response(status_code=404)
    return JSONResponse(json.loads(item), status_code=200)
    
    
@router.post("/items/list")
async def list_notes(request: Request):
    ret = []
    if not db.is_authenticated(request): return Response(status_code=401)
    
    try: path = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, path): return Response(status_code=400)
            
    curr_users_notes = db.note_manager.get_users_notes(request)
    for n in curr_users_notes:               
        if str(n["path"]) == str(path): ret.append(n)
            
    return JSONResponse(status_code=200, content=ret)
    