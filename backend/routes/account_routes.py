from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse

from noterdb import *
from globals import *
from utils import *
from dependency import auth_dependency
from smtputil import Client

db = DB(CONN_LINK())
db.connect()

smtp_login = SMTP_LOGIN()
smtp_client = Client(smtp_login.get("server"), smtp_login.get("port"), smtp_login.get("email"), smtp_login.get("password"))
smtp_client.connect()

router = APIRouter()

@router.post("/items/update/reqpassword")
async def request_password_update(request: Request, is_auth: bool = Depends(auth_dependency)):
    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    
    v_code = str(randint_n(16))
    db.user_manager.update_column(id, "verification_code", v_code)
    smtp_client.send_verification_code(user["email"], v_code)
    
    return Response(status_code=200)
    
    
@router.post("/items/update/reqemail") # JSON EX: {"email":"my_new_email@example.com"}
async def request_email_update(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: email_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)

    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    new_email = email_data["email"]
    
    cur_code = str(randint_n(16))
    new_code = str(randint_n(16))
    
    db.user_manager.update_column(id, "verification_code", f"{cur_code}#{new_code}")
    smtp_client.send_verification_code(user["email"], cur_code)
    smtp_client.send_verification_code(new_email, new_code)
    
    return Response(status_code=200)
    
    
    
    
@router.post("/items/update/password") # JSON EX: {"password":"my_new_password", "code":"123456"}
async def update_password(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: pw_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    
    new_password = hash_password(pw_data["password"])
    in_code = pw_data["code"]
    user_ver_code = str(user["verification_code"]).split("#")[0]
    
    if str(in_code) == user_ver_code:
        db.user_manager.update_column(id, "password", new_password)
        db.user_manager.update_column(id, "verification_code", "")
        return Response(status_code=204) # Valid code - password updated
        
    return Response(status_code=400) # Invalid code
    
    
@router.post("/items/update/email") # JSON EX: {"email":"my_new_email@example.com", "cur_code":"123456", "new_code":"654321"}
async def update_email(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: email_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    
    new_email = email_data["email"]
    cur_code = email_data["cur_code"]
    new_code = email_data["new_code"]
    
    user_ver_code1 = str(user["verification_code"]).split("#")[0] # current email verification code
    user_ver_code2 = str(user["verification_code"]).split("#")[1] # new email verification code
    
    if str(cur_code) == user_ver_code1 and str(new_code) == user_ver_code2:
        db.user_manager.update_column(id, "email", new_email)
        db.user_manager.update_column(id, "verification_code", "")
        return Response(status_code=204) # Valid code - password updated
        
    return Response(status_code=400) # One of the codes are invalid