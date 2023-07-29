import json
from typing import Union

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.noterdb import db
from backend.smtputil import smtp_client
from backend.utils import randint_n, hash_password
from backend.dependency import auth_dependency

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()

@router.post("/items/update/reqpassword")
async def request_password_update(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    id = user.get("id")
    
    v_code = str(randint_n(16))
    if not db.user_manager.update_column(id, "verification_code", v_code): return Response(status_code=400)
    smtp_client.send_verification_code(user["email"], v_code)
    
    return Response(status_code=200)
    
    
@router.post("/items/update/reqemail") # JSON EX: {"email":"my_new_email@example.com"}
async def request_email_update(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    try: email_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    new_email = email_data["email"]

    if db.user_manager.get_user_by_email(new_email) is None:
        id = user.get("id")
        
        cur_code = str(randint_n(16))
        new_code = str(randint_n(16))
        
        if not db.user_manager.update_column(id, "verification_code", f"{cur_code}#{new_code}"): return Response(status_code=400)
        smtp_client.send_verification_code(user["email"], cur_code)
        smtp_client.send_verification_code(new_email, new_code)
        
        return Response(status_code=200)
    
    return Response(status_code=409) # New email already exists on another account
    
    
@router.post("/items/update/password") # JSON EX: {"password":"my_new_password", "code":"123456"}
async def update_password(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    try: pw_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    id = user.get("id")
    
    new_password = hash_password(pw_data["password"])
    in_code = pw_data["code"]
    user_ver_code = str(user["verification_code"]).split("#")[0]
    
    if str(in_code) == user_ver_code:
        if not db.user_manager.update_column(id, "password", new_password): return Response(status_code=400)
        if not db.user_manager.update_column(id, "verification_code", ""): return Response(status_code=400)
        return Response(status_code=204) # Valid code - password updated
        
    return Response(status_code=400) # Invalid code
    
    
@router.post("/items/update/email") # JSON EX: {"email":"my_new_email@example.com", "cur_code":"123456", "new_code":"654321"}
async def update_email(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    try: email_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    id = user.get("id")
    
    new_email = email_data["email"]
    cur_code = email_data["cur_code"]
    new_code = email_data["new_code"]
    
    user_ver_code1 = str(user["verification_code"]).split("#")[0] # current email verification code
    user_ver_code2 = str(user["verification_code"]).split("#")[1] # new email verification code
    
    if str(cur_code) == user_ver_code1 and str(new_code) == user_ver_code2:
        if not db.user_manager.update_column(id, "email", new_email): return Response(status_code=400)
        if not db.user_manager.update_column(id, "verification_code", ""): return Response(status_code=400)
        if not db.user_manager.update_column(id, "email_verified", True): return Response(status_code=400) # true if not already
        return Response(status_code=204) # Valid code - password updated
        
    return Response(status_code=400) # One of the codes are invalid

@router.post("/items/update/name") # JSON EX: {"name":"my_new_name"}
async def update_name(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    try: name_data = await request.json()
    except json.decoder.JSONDecodeError: return (Response(status_code=400))

    new_name = name_data["name"]

    if not db.user_manager.update_column(user.get("id"), "name", new_name): return Response(status_code=400)

    return Response(status_code=204)

@router.post("/items/update/pfp")
async def update_name(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    try: pfp_data = await request.json()
    except json.decoder.JSONDecodeError: return (Response(status_code=400))

    new_pfp = pfp_data["image"]

    if not db.user_manager.update_column(user.get("id"), "pfp", new_pfp): return Response(status_code=400)

    return Response(status_code=204)
    
    
@limiter.limit("3/hour")
@router.post("/resend-verification")
async def resend_verification_email(request: Request, user: Union[bool, dict] = Depends(auth_dependency)):
    m_link = f"http://localhost:8000/verify?id={user.get('id')}"
    
    if smtp_client.send_verification_email(user.get('email'), m_link): return Response(status_code=200)
    else: return Response(status_code=400)
    
    
@router.get("/verify")
async def verify_email(request: Request, id: str):
    if not db.user_manager.update_column(id, "email_verified", True): return Response(status_code=400)
    
    return Response(status_code=204)