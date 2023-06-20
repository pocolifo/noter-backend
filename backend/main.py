import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import makeobjects

app = FastAPI()
API_VERSION = 1


default_user = {
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
# /

def HashPassword(password): return password #insert hash function in the future

def isauthenticated(request: Request) -> bool:
    for u in users:
        if u["id"] == request.cookies.get("authenticate"):
            return True
    return False

@app.delete("/items/delete")
async def deleteitem(request: Request, id_: str):
    if not isauthenticated(request): return JSONResponse(status_code=401, content={})

    for f in folders[0]:
        if f["id"] == id_: folders[0].remove(f) # RemoveElem(folderId, userId)
        return JSONResponse(status_code=204, content={})

    for n in notes[0]:
        if n["id"] == id_: notes[0].remove(n) # RemoveElem(noteId, userId)
        return JSONResponse(status_code=204, content={})
        
    return JSONResponse(status_code=400, content={})

@app.post("/items/create/note")
async def createnote(request: Request):
    noteinfo = await request.json()
    print(noteinfo)
    if not isauthenticated(request): return JSONResponse(status_code=401, content={})

    
    note = make_note(noteinfo[0], noteinfo[1])
    
    notes[0].append(json.loads(note))
    JSONResponse(status_code=201, content=json.loads(note))



@app.post("/items/list")
async def listnotes(request: Request):
    ret_notes = []
    found = False
    print(request.cookies.get("authenticate"))
    if not isauthenticated(request): return JSONResponse(status_code=401, content={})
    
    path = await request.json()
    print(path)
    print(type(path))
    for f in folders[0]: # Just like below, assume the first element will be the correct one
        if f["metadata"]["name"] == path[-1]:
            if f["metadata"]["path"] == path[:-1]: # Remove last element and compare rest of path
                found = True
                break
               
    if not found: return JSONResponse(status_code=400, content={})
            
    
    
                       # WE ARE ASSUMING THE FIRST ELEMENT IS THE CORRECT USERS NOTE LIST
    for n in notes[0]: # UNTIL THERE IS A GetNotes(folderId, userId) db function                  
        if n["metadata"]["path"] == path: ret_notes.append(n)
            
    return JSONResponse(status_code=200, content={ret_notes})    
            





class AuthData(BaseModel):
    email: str
    password: str

@app.post("/authenticate")
async def authenticate(data: AuthData):
    print(data.email)
    print(data.password)
    for u in users:
        if u["email"] == data.email and u["pass"] == HashPassword(data.password):
            response = JSONResponse(status_code=200, content={"authenticated": True})
            print("AUTHENTICATED")
            response.set_cookie(key="authenticate", value=str(u["id"]), path="/", max_age=180000, httponly=True)
            print(u["id"])
            return response
            #return JSONResponse(status_code=200, content={"authenticated": True})
    return {"authenticated": False}
    

@app.get("/")
async def root(request: Request):
    print(request.cookies.get("authenticate"))
    if not isauthenticated(request):
        return JSONResponse(status_code=200, content={"apiVersion": API_VERSION, "user":0})
    for u in users:
        if u["id"] == request.cookies.get("authenticate"):
            return JSONResponse(status_code=200, content=u) # add API version to response content

@app.get("/cookies")
async def sendcookies(request: Request):
    if not isauthenticated(request): return JSONResponse(status_code=401, content={})
    return request.cookies



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)