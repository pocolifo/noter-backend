from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *

db = DB(CONN_LINK())
db.connect()

router = APIRouter()

@router.post("/items/update/metadata")
async def update_metadata(request: Request, id: str):
    try: updateinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return JSONResponse(status_code=401, content={})
    if not db.does_path_exist(request, updateinfo["path"]): return Response(status_code=400)
    
    db.update_metadata_by_id(request, id, updateinfo["name"], updateinfo["path"])
            
    return Response(status_code=204)
    
    
@router.put("/items/update/blocks")
async def update_blocks(request: Request, id: str):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return Response(status_code=401)

    db.update_blocks_by_id(request, id, json.dumps(newblockinfo))
    
    return Response(status_code=204)
    
    
@router.post("/items/update/notedata")
async def set_notedata(request: Request, id:str):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    db.set_notedata_by_id(newblockinfo["data"], id)
    
    
    return Response(status_code=204)