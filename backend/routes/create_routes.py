from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask

from noterdb import *
from smtputil import Client
from globals import *
from make_objects import *
from utils import *
from dependency import auth_dependency

db = DB(CONN_LINK())
db.connect()

smtp_login = SMTP_LOGIN()
smtp_client = Client(smtp_login.get("server"), smtp_login.get("port"), smtp_login.get("email"), smtp_login.get("password"))
smtp_client.connect()

router = APIRouter()

@router.post("/items/create/user")
async def create_user(request: Request):
    try: userinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if len(db.user_manager.get_users_by_email(userinfo["email"])) == 0:
        user = make_user(userinfo["email"], hash_password(userinfo["password"]))
        db.user_manager.insert_user(user)
        user.pop("password")
        
        m_link = f"http://localhost:8000/verify?id={user.get('id')}"
        task = BackgroundTask(smtp_client.send_verification_email, to=user.get("email"), link=m_link)
        
        response = JSONResponse(status_code=200, content=user, background=task)
        response.set_cookie(key="authenticate", value=to_jwt(str(user.get("id"))), path="/") # auth on creation
        return response
        
    return Response(status_code=400) # account with email already exists
    
    
@router.post("/items/create/note")
async def create_note(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    if not db.folder_manager.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], False)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/studyguide")
async def create_studyguide(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], True)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/folder") 
async def create_folder(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: folderinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.folder_manager.does_path_exist(request, folderinfo["path"]): return Response(status_code=400)
    
    folder = make_folder(request, folderinfo["name"], folderinfo["path"])
    db.folder_manager.insert_folder(folder)
    return JSONResponse(status_code=201, content=folder)