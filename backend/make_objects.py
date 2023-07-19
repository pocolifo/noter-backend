import os
from uuid import uuid4
from datetime import datetime
from starlette.requests import Request
from json import dumps as jsondumps

from noterdb import *
from globals import *
from utils import *
import stripe

db = DB(CONN_LINK())
db.connect()

def make_user(email: str, password: str):
    stripe_customer = stripe.Customer.create(
        email=email
    )
    
    return {
        "id":str(uuid4()),
        "email":email,
        "password":password,
        "stripe_id": stripe_customer.id,
        "lastSignedIn":str(datetime.now().isoformat()),
        "joinedOn":str(datetime.now().isoformat()),
        "history":[],
        "email_verified":False,
        "plan_id":"",
        "has_noter_access": False
    }

def make_note(request: Request, name: str, path: list, studyguide: bool):
    type_ = "studyguide" if studyguide else "note"
    return {
        "id":str(uuid4()),
        "type":type_,
        "name":name,
        "path":path,
        "lastEdited":"",
        "createdOn":str(datetime.now().isoformat()),
        "owner":from_jwt(str(request.cookies.get("authenticate"))),
        "blocks":[]
    }

def make_folder(request: Request, name: str, path: list):
    return {
        "id":str(uuid4()),
        "type":"folder",
        "name":name,
        "path":path,
        "lastEdited":"",
        "createdOn":str(datetime.now().isoformat()),
        "owner":from_jwt(str(request.cookies.get("authenticate")))
    }
    


