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
async def request_update_password(request: Request, is_auth: bool = Depends(auth_dependency)):
    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    
    v_code = str(randint_n(16))
    db.user_manager.update_verification_code(id, v_code)
    smtp_client.send_verification_code(user["email"], v_code)
    
    return Response(status_code=200)
    
    
@router.post("/items/update/password") # JSON EX: {"password":"my_new_password", "code":"123456"}
async def update_password(request: Request, is_auth: bool = Depends(auth_dependency)):
    try: pw_data = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    id = from_jwt(str(request.cookies.get("authenticate")))
    user = json.loads(db.user_manager.get_user_data_by_id(id))
    
    new_password = hash_password(pw_data["password"])
    in_code = pw_data["code"]
    
    if str(in_code) == str(user["verification_code"]):
        db.user_manager.update_password(id, new_password)
        db.user_manager.update_verification_code(id, "")
        return Response(status_code=204) # Valid code - password updated
        
    return Response(status_code=400) # Invalid code
    
    
    
    
    
    
    
    