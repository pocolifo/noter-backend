import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from starlette.requests import Request

from backend.utils import from_jwt
from backend.tables import User, Note, Folder

class BaseManager:
    def __init__(self, session):
        self.session = session

class UserManager(BaseManager):
    def get_user_data_by_id(self, id: str):
        user = self.session.query(User).filter(User.id == id).first()
            
        if user is not None:
            return json.dumps({
                'id': user.id,
                'email': user.email,
                'password': user.password,
                'name': user.name,
                'pfp': user.pfp,
                'stripe_id': user.stripe_id,
                'last_signed_in': user.last_signed_in,
                'joined_on': user.joined_on,
                'history': user.history,
                'email_verified': user.email_verified,
                'has_noter_access': user.has_noter_access,
                'verification_code': user.verification_code
            })
            
        return False

    def insert_user(self, user: dict):
        user_obj = User(
            id=user.get('id'),
            email=user.get('email'),
            password=user.get('password'),
            name=user.get('name'),
            pfp=user.get('pfp'),
            stripe_id=user.get('stripe_id'),
            last_signed_in=user.get('last_signed_in'),
            joined_on=user.get('joined_on'),
            history=user.get('history'),
            email_verified=user.get('email_verified'),
            has_noter_access=user.get('has_noter_access'),
            verification_code=user.get('verification_code')
        )
        self.session.add(user_obj)
        self.session.commit()

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter(User.email == email).first()
        
        if user is None: return None
        return {"id": user.id, "email": user.email, "password": user.password, "name": user.name,
                "pfp": user.pfp, "stripe_id": user.stripe_id, "last_signed_in": user.last_signed_in,
                "joined_on": user.joined_on, "history": user.history, "email_verified": user.email_verified,
                "has_noter_access": user.has_noter_access, "verification_code": user.verification_code}

    def get_users_notes(self, request: Request):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        notes = self.session.query(Note).filter(Note.owner_id == user_id).all()
        return [{"id": note.id, "type": note.type, "name": note.name, "path": note.path,
            "last_edited": note.last_edited, "created_on": note.created_on, "blocks": note.blocks} for note in notes]
    
    def get_users_folders(self, request: Request):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        folders = self.session.query(Folder).filter(Folder.owner_id == user_id).all()
        return [{"id": folder.id, "type": "folder", "name": folder.name, "path": folder.path,
            "last_edited": folder.last_edited, "created_on": folder.created_on} for folder in folders]
    
    def update_column(self, user_id, column_name, column_value):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is not None:
            setattr(user, column_name, column_value)
            self.session.commit()
            return True
        return False
        

class NoteManager(BaseManager):
    def insert_note(self, note: dict):
        note_obj = Note(
            id=note.get('id'),
            type=note.get('type'),
            name=note.get('name'),
            path=note.get('path'),
            last_edited=note.get('last_edited'),
            created_on=note.get('created_on'),
            owner_id=note.get('owner'),
            blocks=note.get('blocks')
        )
        self.session.add(note_obj)
        self.session.commit()

    def update_blocks_by_id(self, request: Request, id: str, new_blocks: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))

        notes = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).all()

        for note in notes:
            note.blocks = json.loads(new_blocks)
            note.last_edited = datetime.now().isoformat()

        self.session.commit()
        
    def get_note_by_id(self, request: Request, id:str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
    
        note = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()
        if note is None: return False
        
        return {
        "id":note.id,
        "type":note.type,
        "name":note.name,
        "path":note.path,
        "last_edited":note.last_edited,
        "created_on":note.created_on,
        "owner_id":note.owner_id,
        "blocks":note.blocks
        }
        
        

    
class FolderManager(BaseManager):
    def does_path_exist(self, request: Request, fullpath: list):
        if len(fullpath) == 0: 
            return True

        user_id = from_jwt(str(request.cookies.get("authenticate")))
        folders = self.session.query(Folder).filter(Folder.owner_id == user_id).all()

        for folder in folders:
            if folder.id == fullpath[-1] and folder.path == fullpath[:-1]:
                return True

        return False

    def insert_folder(self, folder: dict):
        folder_obj = Folder(
            id=folder.get('id'),
            name=folder.get('name'),
            path=folder.get('path'),
            last_edited=folder.get('last_edited'),
            created_on=folder.get('created_on'),
            owner_id=folder.get('owner')
        )
        self.session.add(folder_obj)
        self.session.commit()

class DB:
    def __init__(self, conn_link: str):
        self.Session = None
        self.engine = None
        self.session = None
        
        self.user_manager = None
        self.note_manager = None
        self.folder_manager = None
        
        self.conn_link = conn_link


    def connect(self): # Returns True if connection to database is successful
        try:
            self.engine = create_engine(self.conn_link)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            
            self.user_manager = UserManager(self.session)
            self.note_manager = NoteManager(self.session)
            self.folder_manager = FolderManager(self.session)
            
            return True
        except Exception:
            return False

        
    def is_authenticated(self, request: Request) -> bool:
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        user = self.session.query(User).filter(User.id == user_id).first()
        return user is not None


    def get_item(self, request: Request, id: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))

        note = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()

        if note is not None:
            return json.dumps({
                'id': note.id,
                'type': note.type,
                'name': note.name,
                'path': note.path,
                'last_edited': note.last_edited,
                'created_on': note.created_on,
                'owner_id': note.owner_id,
                'blocks': note.blocks
            })

        folder = self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).first()

        if folder is not None:
            return json.dumps({
                'id': folder.id,
                'name': folder.name,
                'path': folder.path,
                'last_edited': folder.last_edited,
                'created_on': folder.created_on,
                'owner_id': folder.owner_id,
            })

        return False


    def delete_item_by_id(self, request: Request, id: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))

        self.session.query(Note).filter(Note.path.any(id), Note.owner_id == user_id).delete()
        self.session.query(Folder).filter(Folder.path.any(id), Folder.owner_id == user_id).delete()

        self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).delete()
        self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).delete()
        
        self.session.commit()


    def update_metadata_by_id(self, request: Request, id: str, new_name: str, new_path: list):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
      
        notes = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).all()
        folders = self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).all()

        for note in notes:
            note.name = new_name
            note.path = new_path
            note.last_edited = datetime.now().isoformat()

        for folder in folders:
            folder.name = new_name
            folder.path = new_path
            folder.last_edited = datetime.now().isoformat()

        self.session.commit()

db = DB(os.environ['SQLALCHEMY_URL'])
db.connect()