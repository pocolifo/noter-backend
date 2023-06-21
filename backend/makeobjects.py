from uuid import uuid4
from datetime import datetime

def make_note(name: str, path: list, studyguide: bool): # update more info as db is created
    type_ = "studyguide" if studyguide else "note"
    newnote = '''
{{
    "id": "{0}",
    "type": "{1}",
    "metadata": {{
        "name": "{2}",
        "path": "{3}",
        "lastEdited": "",
        "createdOn": "{4}",
        "owner": {{
            "id": "90da6511-685e-4538-a2cf-19c112616c8f",
            "email": "example@example.com",
            "pass": "htw7g8h234bsj",
            "lastSignedIn": "2023-06-19T01:17:05.565Z",
            "joinedOn": "2023-06-19T01:17:05.565Z",
            "history": [
                {{
                    "type": "studentTypeSurveyResponse",
                    "timestamp": "2023-06-19T01:17:05.565Z",
                    "data": {{
                        "responded": "college"
                    }}
                }}
            ]
        }}
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
'''.format(str(uuid4()), type_, name, str(path), datetime.now().isoformat())
    return newnote

def make_folder(name: str, path: list): # update more info as db is created
    new_folder = '''
{{
    "id": "{0}",
    "type": "folder",
    "metadata": {{
        "name": "{1}",
        "path": "{2}",
        "lastEdited": "",
        "createdOn": "{3}",
        "owner": {{
            "id": "90da6511-685e-4538-a2cf-19c112616c8f",
            "email": "example@example.com",
            
            "lastSignedIn": "2023-06-19T01:17:05.565Z",
            "joinedOn": "2023-06-19T01:17:05.565Z",
            "history": [
                {{
                    "type": "studentTypeSurveyResponse",
                    "timestamp": "2023-06-19T01:17:05.565Z",
                    "data": {{
                        "responded": "college"
                    }}
                }}
            ]
        }}
    }}
}}
'''.format(str(uuid4()), name, str(path), datetime.now().isoformat())
    return new_folder








