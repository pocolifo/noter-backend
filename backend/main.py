import uvicorn, json
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from makeobjects import make_note, make_folder
from utils import get_current_isodate, hash_password

app = FastAPI()
API_VERSION = 1

default_user = { # USE THE EMAIL AND PASSWORD HERE FOR /authenticate
    "id": "90da6511-685e-4538-a2cf-19c112616c8f",
    "email": "example@example.com",
    "pass": "htw7g8h234bsj",
    "lastSignedIn": "2023-06-19T01:17:05.565Z",
    "joinedOn": "2023-06-19T01:17:05.565Z",
    "history": [
        {
            "type": "studentTypeSurveyResponse",
            "timestamp": "2023-06-19T01:17:05.565Z",
            "data": {
                "responded": "college"
            }
        }
    ]
}

# MOCK DATABASE
users = [default_user] #GetUserList(database)
notes = [[], []]
folders = [[], []]

def does_path_exist(fullpath: list):
    if len(fullpath) == 0: return True
    for f in folders[0]: # Just like below, assume the first element will be the correct one
        if str(f["metadata"]["name"]) == str(fullpath[-1]):
            if str(f["metadata"]["path"]) == str(fullpath[:-1]): # Remove last element and compare rest of path
                return True
    return False
    
def is_authenticated(request: Request) -> bool:
    for u in users:
        if u["id"] == request.cookies.get("authenticate"):
            return True
    return False
############## /

@app.post("/items/create/note")
async def create_note(request: Request):
    noteinfo = await request.json()
    
    if not is_authenticated(request): return Response(status_code=401)
    if not does_path_exist(noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(noteinfo["name"], noteinfo["path"], False)
    
    notes[0].append(json.loads(str(note)))
    return JSONResponse(status_code=201, content=json.loads(note))


@app.post("/items/create/studyguide")
async def create_studyguide(request: Request):
    noteinfo = await request.json()
    
    if not is_authenticated(request): return Response(status_code=401)
    if not does_path_exist(noteinfo["path"]): return Response(status_code=400)
    
    note = make_note(noteinfo["name"], noteinfo["path"], True)
    
    notes[0].append(json.loads(note))
    return JSONResponse(status_code=201, content=json.loads(note))


@app.post("/items/create/folder") 
async def create_folder(request: Request):
    folderinfo = await request.json()
    
    if not is_authenticated(request): return Response(status_code=401)
    if not does_path_exist(folderinfo["path"]): return Response(status_code=400)
    
    folder = make_folder(folderinfo["name"], folderinfo["path"])
    
    folders[0].append(json.loads(folder))
    return JSONResponse(status_code=201, content=json.loads(folder))

@app.delete("/items/delete")
async def delete_item(request: Request, id: str):
    if not is_authenticated(request): return Response(status_code=401)

    for f in folders[0]:
        if f["id"] == id: folders[0].remove(f) # RemoveElem(folderId, userId)
        return Response(status_code=204)

    for n in notes[0]:
        if n["id"] == id: notes[0].remove(n) # RemoveElem(noteId, userId)
        return Response(status_code=204)
        
    return Response(status_code=400)


@app.post("/items/update/metadata")
async def update_metadata(request: Request, id: str):
    updateinfo = await request.json()
    
    if not is_authenticated(request): return JSONResponse(status_code=401, content={})
    if not does_path_exist(updateinfo["path"]): return Response(status_code=400)
    
    for f in folders[0]:
        if f["id"] == id:
            f["metadata"]["name"] = updateinfo["name"]
            f["metadata"]["path"] = updateinfo["path"]
            f["metadata"]["lastEdited"] = get_current_isodate()
            
            return Response(status_code=204)

    for n in notes[0]:
        if n["id"] == id:
            n["metadata"]["name"] = updateinfo["name"]
            n["metadata"]["path"] = updateinfo["path"]
            n["metadata"]["lastEdited"] = get_current_isodate()
            
            return Response(status_code=204)
            
    return Response(status_code=204)
    
    
@app.put("/items/update/blocks")
async def update_blocks(request: Request, id: str):
    newblockinfo = await request.json()
    
    if not is_authenticated(request): return Response(status_code=401)

    for n in notes[0]:
        if n["id"] == id:
            n["blocks"] = newblockinfo
            n["metadata"]["lastEdited"] = get_current_isodate()
            return Response(status_code=204)
    return Response(status_code=204)
    
    
    
@app.post("/items/list")
async def list_notes(request: Request):
    ret_notes = []
    if not is_authenticated(request): return Response(status_code=401)
    
    path = await request.json()
    
    if not does_path_exist(path): return Response(status_code=400)
            
    
                       # WE ARE ASSUMING THE FIRST ELEMENT IS THE CORRECT USERS NOTE LIST
    for n in notes[0]: # UNTIL THERE IS A GetNotes(folderId, userId) db function                  
        if str(n["metadata"]["path"]) == str(path): ret_notes.append(n)
            
    return JSONResponse(status_code=200, content=ret_notes)    
            

class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(data: AuthData):
    for u in users:
        if u["email"] == data.email and u["pass"] == hash_password(data.password):
            u["lastSignedIn"] = get_current_isodate()
            response = JSONResponse(status_code=200, content={"authenticated": True})
            response.set_cookie(key="authenticate", value=str(u["id"]), path="/")
            return response
            
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    if not is_authenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION, "user":0})
    for u in users:
        if u["id"] == request.cookies.get("authenticate"):
            return JSONResponse(status_code=200, content=u) # add API version to response content


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)