import uvicorn, json
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from makeobjects import make_note, make_folder
from utils import get_current_isodate, hash_password
from noterdb import DB

app = FastAPI()
API_VERSION = 1

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""

db = DB(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)
try: db.connect()
except:
    print("COULD NOT CONNECT TO DATABASE!")
    exit(0)


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
   
   
@app.get("/items/{id}")
async def get_item(request: Request, id: str):
    if not db.is_authenticated(request): return Response(status_code=401)

    item = db.get_item(request, id)
    if not item: return Response(status_code=404)
    return JSONResponse(json.loads(item), status_code=200)

    
@app.post("/items/create/note")
async def create_note(request: Request):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return Response(status_code=401)
    if not db.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], False)
    
    db.insert_note(note)
    return JSONResponse(status_code=201, content=json.loads(note))


@app.post("/items/create/studyguide")
async def create_studyguide(request: Request):
    try: noteinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return Response(status_code=401)
    if not db.does_path_exist(request, noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(request, noteinfo["name"], noteinfo["path"], True)
    
    db.insert_note(note)
    return JSONResponse(status_code=201, content=json.loads(note))


@app.post("/items/create/folder") 
async def create_folder(request: Request):
    try: folderinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return Response(status_code=401)
    if not db.does_path_exist(request, folderinfo["path"]): return Response(status_code=400)
    
    folder = make_folder(request, folderinfo["name"], folderinfo["path"])
    
    db.insert_folder(folder)
    return JSONResponse(status_code=201, content=json.loads(folder))

@app.delete("/items/delete")
async def delete_item(request: Request, id: str):
    if not db.is_authenticated(request): return Response(status_code=401)

    db.delete_item_by_id(request, id)
    return Response(status_code=204)
        
    #return Response(status_code=400)


@app.post("/items/update/metadata")
async def update_metadata(request: Request, id: str):
    try: updateinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return JSONResponse(status_code=401, content={})
    if not db.does_path_exist(request, updateinfo["path"]): return Response(status_code=400)
    
    db.update_metadata_by_id(request, id, updateinfo["name"], updateinfo["path"])
            
    return Response(status_code=204)
    
    
@app.put("/items/update/blocks")
async def update_blocks(request: Request, id: str):
    try: newblockinfo = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.is_authenticated(request): return Response(status_code=401)

    db.update_blocks_by_id(request, id, json.dumps(newblockinfo))
    
    return Response(status_code=204)
    

@app.post("/items/list")
async def list_notes(request: Request):
    ret = []
    if not db.is_authenticated(request): return Response(status_code=401)
    
    try: path = await request.json()
    except json.decoder.JSONDecodeError: return Response(status_code=400)
    
    if not db.does_path_exist(request, path): return Response(status_code=400)
            
    curr_users_notes = db.get_users_notes(request)
    for n in curr_users_notes:               
        if str(n["metadata"]["path"]) == str(path): ret.append(n)
            
    return JSONResponse(status_code=200, content=ret)    
            

class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(request: Request, data: AuthData):
    pusers = db.get_users_by_email(data.email)

    for u in pusers:
        if u["email"] == data.email and u["pass"] == hash_password(data.password):
            u["lastSignedIn"] = get_current_isodate() # UPDATE IN DB
            response = JSONResponse(status_code=200, content={"authenticated": True})
            response.set_cookie(key="authenticate", value=str(u["id"]), path="/")
            db.update_lastsignedin(request)
            return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not db.is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION, "user":0})
        
    udata = db.get_user_data_by_id(request.cookies.get("authenticate"))
    return JSONResponse(status_code=200, content=udata) # add API version to response content


