from uuid import uuid4
from datetime import datetime

def make_note(name: str, path: list): # update more info as db is created
    newnote = """
{
    "id": {},
    "type": "note",
    "metadata": {
        "name": {},
        "path": {},
        "lastEdited": "",
        "createdOn": {},
        "owner": {
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
    },
    "blocks": [
        {
            "type": "text",
            "data": {
                "content": "<serialized data>"
            }
        },
        {
            "type": "image",
            "data": {
                "url": "<serialized URL data>"
            }
        }
    ]
}
""".format(str(uuid4()), name, str(path), datetime.now().isoformat())