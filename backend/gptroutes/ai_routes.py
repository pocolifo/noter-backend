import openai
from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from typing import Union

from noterdb import *
from globals import *
from dependency import auth_dependency

db = DB(CONN_LINK())
db.connect()

router = APIRouter()

openai.api_key = os.environ.get('OPENAI_SECRET_KEY')

SUMMARIZE_PROMPT = "Summarize the following text, get right into the summary. Do not use first person pronouns."
BULLET_PROMPT = "Summarize the following text into a markdown style list of bullet points. Do not use first person pronouns."

def gpt35_turbo(sysprompt: str, userprompt: str):
    res = str(openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": userprompt}
        ]
    ))

    jres = json.loads(res)

    return str(jres["choices"][0]["message"]["content"])

@router.post("/ai/generate/summary")
async def generate_summary(request: Request, id:str, is_auth: Union[bool, dict] = Depends(auth_dependency)):

    sentences = ""
    
    note = db.note_manager.get_note_by_id(request, id)
    blocks = note["blocks"]
    for b in blocks:
        if b["type"] == "text" or b["type"] == "header":
            sentences += str(b["data"]["content"]+" ")
            
    summarization = gpt35_turbo(SUMMARIZE_PROMPT, sentences)
    
    
    md_bullets = gpt35_turbo(BULLET_PROMPT, sentences)
    bullets = md_bullets.split("\n")
    bullets = [b.replace("- ", "") for b in bullets]
    
    return JSONResponse(status_code=200, content={"bullets":bullets, "sentences":summarization})
        
    
    
    
    
    
    
    
    
    
    