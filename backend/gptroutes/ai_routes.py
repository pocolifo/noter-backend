import os
import json
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response
import openai

from backend.noterdb import db
from backend.dependency import auth_dependency

router = APIRouter()

SUMMARIZE_PROMPT = "Summarize the following text, get right into the summary. Do not use first person pronouns."
BULLET_PROMPT = "Summarize the following text into a markdown style list of bullet points. Do not use first person pronouns."

def quiz_prompt(n: int):
    if type(n) == int:
        return """Generate {0} multiple choice questions about the following text. Respond using the following JSON schema:\n
[
  {{
     'question': 'question',
     'options': [
       'answer 1',
       'answer 2',
       'answer 3',
       'answer 4'
      ],
      'correct': 3
  }}
]

Note that 'correct' is an index of 'options' that starts with 0.
Respond in PURE Json.
Do not use first person pronouns.
\n""".format(str(n))

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
        
    
@router.post("/ai/generate/quiz")
async def generate_quiz(request: Request, id:str, n:int, is_auth: Union[bool, dict] = Depends(auth_dependency)):
    sentences = ""
    
    note = db.note_manager.get_note_by_id(request, id)
    blocks = note["blocks"]
    for b in blocks:
        if b["type"] == "text" or b["type"] == "header":
            sentences += str(b["data"]["content"]+" ")
            
    try: quiz = json.loads(gpt35_turbo(quiz_prompt(n), sentences))
    except Exception: return Response(status_code=400)
    
    return JSONResponse(status_code=200, content=quiz)
    