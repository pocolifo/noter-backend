import json
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.background import BackgroundTask
from backend.models.requests import CreateStudyGuideRequest, ItemMetadataRequest, UserCredentialsRequest

from backend.noterdb import db
from backend.smtputil import smtp_client
from backend.make_objects import make_folder, make_note, make_user
from backend.utils import hash_password, to_jwt, clean_udata
from backend.dependency import auth_dependency

router = APIRouter()

@router.post("/items/create/user")
async def create_user(request: Request, creds: UserCredentialsRequest):
    if db.user_manager.get_user_by_email(creds.email) is None:
        user = make_user(creds.email, hash_password(creds.password))
        db.user_manager.insert_user(user)
        user = clean_udata(user)
        
        m_link = f"http://localhost:8000/verify?id={user.get('id')}"
        task = BackgroundTask(smtp_client.send_verification_email, to=creds.email, link=m_link)
        
        response = JSONResponse(status_code=200, content=user, background=task)
        response.set_cookie(key="authenticate", value=to_jwt(str(user.get("id"))), path="/") # auth on creation
        return response
        
    return Response(status_code=400) # account with email already exists
    
    
@router.post("/items/create/note")
async def create_note(request: Request, new_note: ItemMetadataRequest, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    if not db.folder_manager.does_path_exist(request, new_note.path):
        return Response(status_code=400)
    
    note = make_note(request, new_note.name, new_note.path, False)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/studyguide")
async def create_studyguide(request: Request, new_study_guide: CreateStudyGuideRequest, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    if not db.folder_manager.does_path_exist(request, new_study_guide.path):
        return Response(status_code=400)
    
    note = make_note(request, new_study_guide.name, new_study_guide.path, True)
    db.note_manager.insert_note(note)
    return JSONResponse(status_code=201, content=note)


@router.post("/items/create/folder") 
async def create_folder(request: Request, new_folder: ItemMetadataRequest, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    if not db.folder_manager.does_path_exist(request, new_folder.path):
        return Response(status_code=400)
    
    folder = make_folder(request, new_folder.name, new_folder.path)
    db.folder_manager.insert_folder(folder)
    return JSONResponse(status_code=201, content=folder)