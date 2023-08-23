import json
from typing import Union

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response

from backend.models.requests import ItemMetadataRequest
from backend.noterdb import DB, db
from backend.dependency import auth_dependency
from backend.utils import from_jwt

router = APIRouter()

@router.post("/items/update/metadata")
async def update_metadata(request: Request, update_info: ItemMetadataRequest, id: str, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    if not await db.folder_manager.does_path_exist(request, update_info.path):
        return Response(status_code=400)

    await db.update_metadata_by_id(request, id, update_info.name, update_info.path)
            
    return Response(status_code=204)
    

# TODO: properly check, validate, sanitize newblockinfo on the server
@router.put("/items/update/blocks")
async def update_blocks(request: Request, id: str, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    await db.note_manager.update_blocks_by_id(request, id, json.dumps(newblockinfo))
    
    return Response(status_code=204)
    
    
@router.delete("/items/delete")
async def delete_item(request: Request, id: str, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    await db.delete_item_by_id(request, id)
    return Response(status_code=204)
        
    #return Response(status_code=400)
    
@router.delete("/items/user/delete")
async def delete_user(request: Request, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    user_id = from_jwt(str(request.cookies.get("authenticate")))
    if not await db.user_manager.delete(user_id): return Response(status_code=400)
    return Response(status_code=204)
        
    #return Response(status_code=400)