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

@router.post("/items/update/metadata")
async def update_metadata(request: Request, id: str, is_auth: bool = Depends(auth_dependency)):
    try: updateinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, updateinfo["path"]): return Response(status_code=400)

    db.update_metadata_by_id(request, id, str(updateinfo["name"]), updateinfo["path"])
            
    return Response(status_code=204)
    
    
@router.put("/items/update/blocks")
async def update_blocks(request: Request, id: str, is_auth: bool = Depends(auth_dependency)):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    db.note_manager.update_blocks_by_id(request, id, json.dumps(newblockinfo))
    
    return Response(status_code=204)
    
    
@router.get("/verify")
async def verify_email(request: Request, id: str):
    update = db.user_manager.update_email_verified(request, id)
    if not update: return Response(status_code=400)
    
    return Response(status_code=204)