from uuid import uuid4
from datetime import datetime
from starlette.requests import Request
from noterdb import DB
from json import dumps as jsondumps

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

def make_note(request: Request, name: str, path: list, studyguide: bool): # update more info as db is created
    type_ = "studyguide" if studyguide else "note"
    newnote = '''
{{
    "id": "{0}",
    "type": "{1}",
    "metadata": {{
        "name": "{2}",
        "path": {3},
        "lastEdited": "",
        "createdOn": "{4}",
        "owner": {5}
            
    }},
    "blocks": [
        {{
            "type": "text",
            "data": {{
                "content": "<serialized data>"
            }}
        }},
        {{
            "type": "image",
            "data": {{
                "url": "<serialized URL data>"
            }}
        }}
    ]
}}
'''.format(str(uuid4()), type_, name, jsondumps(path), datetime.now().isoformat(),
            db.get_user_data_by_id(str(request.cookies.get("authenticate"))))
    return newnote

def make_folder(request: Request, name: str, path: list): # update more info as db is created
    new_folder = '''
{{
    "id": "{0}",
    "type": "folder",
    "metadata": {{
        "name": "{1}",
        "path": {2},
        "lastEdited": "",
        "createdOn": "{3}",
        "owner": {4}
            
    }}
}}
'''.format(str(uuid4()), name, jsondumps(path), datetime.now().isoformat(),
            db.get_user_data_by_id(str(request.cookies.get("authenticate"))))
    return new_folder





