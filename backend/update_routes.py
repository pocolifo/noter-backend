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
    
    if not db.folder_manager.does_path_exist(request, updateinfo["path"]): return Response(status_code=400)

    db.update_metadata_by_id(request, id, str(updateinfo["name"]), updateinfo["path"])
            
    return Response(status_code=204)
    
    
@router.put("/items/update/blocks")
async def update_blocks(request: Request, id: str):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    db.note_manager.update_blocks_by_id(request, id, json.dumps(newblockinfo))
    
    return Response(status_code=204)
    
    
@router.post("/verify")
async def verify_email(request: Request, id: str):
    # Will return 400 if verifying a user you aren't authenticated on
    update = db.user_manager.update_email_verified(request, id)
    if not update: return Response(status_code=400)
    
    return Response(status_code=204)