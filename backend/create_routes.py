from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *
from make_objects import *
from utils import *

db = DB(CONN_LINK())
db.connect()

router = APIRouter()

@router.post("/items/create/user")
async def create_user(request: Request):
    try: userinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if len(db.user_manager.get_users_by_email(userinfo["email"])) == 0:
        user = make_user(userinfo["email"], hash_password(userinfo["password"]))
        db.user_manager.insert_user(user)
        return JSONResponse(status_code=201, content=user)
        
    return Response(status_code=400) # account with email already exists
    
    
@router.post("/items/create/note")
async def create_note(request: Request):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    if not db.folder_manager.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], False)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/studyguide")
async def create_studyguide(request: Request):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], True)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/folder") 
async def create_folder(request: Request):
    try: folderinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, folderinfo["path"]): return Response(status_code=400)
    
    folder = make_folder(request, folderinfo["name"], folderinfo["path"])
    db.folder_manager.insert_folder(folder)
    return JSONResponse(status_code=201, content=folder)