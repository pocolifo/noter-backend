import json
import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from starlette.requests import Request

from backend.utils import from_jwt, is_valid_uuid4
from backend.tables import User, Note, Folder

class BaseManager:
    def __init__(self, session):
        self.session = session
        
    @contextmanager
    def open_session(self):
        session = self.session
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

class UserManager(BaseManager):
    def get_user_data_by_id(self, id: str):
        with self.open_session() as session:
            user = session.query(User).filter(User.id == id).first()
                
            if user is not None:
                return json.dumps({
                    'id': user.id,
                    'email': user.email,
                    'password': user.password,
                    'name': user.name,
                    'pfp': user.pfp,
                    'stripe_id': user.stripe_id,
                    'last_signed_in': str(user.last_signed_in),
                    'joined_on': str(user.joined_on),
                    'history': user.history,
                    'email_verified': user.email_verified,
                    'has_noter_access': user.has_noter_access,
                    'verification_code': user.verification_code
                })
                
            return False

    def insert_user(self, user: dict):
        with self.open_session() as session:
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
            session.add(user_obj)
            session.commit()

    def get_user_by_email(self, email: str):
        with self.open_session() as session:
            user = session.query(User).filter(User.email == email).first()
            
            if user is None: return None
            return {"id": user.id, "email": user.email, "password": user.password, "name": user.name,
                    "pfp": user.pfp, "stripe_id": user.stripe_id, "last_signed_in": str(user.last_signed_in),
                    "joined_on": str(user.joined_on), "history": user.history, "email_verified": user.email_verified,
                    "has_noter_access": user.has_noter_access, "verification_code": user.verification_code}

    def get_users_notes(self, request: Request):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        with self.open_session() as session:
            notes = session.query(Note).filter(Note.owner_id == user_id).all()
            return [{"id": note.id, "type": note.type, "name": note.name, "path": note.path,
                "last_edited": str(note.last_edited), "created_on": str(note.created_on), "blocks": note.blocks} for note in notes]
    
    def get_users_folders(self, request: Request):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        with self.open_session() as session:  
            folders = session.query(Folder).filter(Folder.owner_id == user_id).all()
            return [{"id": folder.id, "type": "folder", "name": folder.name, "path": folder.path,
                "last_edited": str(folder.last_edited), "created_on": str(folder.created_on)} for folder in folders]
    
    def update_column(self, user_id, column_name, column_value):
        if not is_valid_uuid4(user_id): return False
            
        with self.open_session() as session:
            user = session.query(User).filter(User.id == str(user_id)).first()
            if user is not None:
                setattr(user, column_name, column_value)
                session.commit()
                return True
            return False
        
    def delete_user(self, user_id: str):
        with self.open_session() as session:
            try:
                # Remove items with foreign key relationships first
                session.query(Note).filter(Note.owner_id == user_id).delete()
                session.query(Folder).filter(Folder.owner_id == user_id).delete()
                # Then remove user
                session.query(User).filter(User.id == user_id).delete()
                session.commit()
                return True
            except Exception:
                session.rollback()
                return False

        
class NoteManager(BaseManager):
    def insert_note(self, note: dict):
        with self.open_session() as session:
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
            session.add(note_obj)
            session.commit()

    def update_blocks_by_id(self, request: Request, id: str, new_blocks: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
        with self.open_session() as session:
            notes = session.query(Note).filter(Note.id == id, Note.owner_id == user_id).all()

            for note in notes:
                note.blocks = json.loads(new_blocks)
                note.last_edited = datetime.now().isoformat()

            session.commit()
        
    def get_note_by_id(self, request: Request, id:str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
    
        with self.open_session() as session:
            note = session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()
            if note is None: return False
            
            return {
                "id":note.id,
                "type":note.type,
                "name":note.name,
                "path":note.path,
                "last_edited":str(note.last_edited),
                "created_on":str(note.created_on),
                "owner_id":note.owner_id,
                "blocks":note.blocks
            }
        
        

    
class FolderManager(BaseManager):
    def does_path_exist(self, request: Request, fullpath: list):
        if len(fullpath) == 0: 
            return True

        user_id = from_jwt(str(request.cookies.get("authenticate")))
        with self.open_session() as session:
            folders = session.query(Folder).filter(Folder.owner_id == user_id).all()

            for folder in folders:
                if folder.id == fullpath[-1] and folder.path == fullpath[:-1]:
                    return True

            return False

    def insert_folder(self, folder: dict):
        with self.open_session() as session:
            folder_obj = Folder(
                id=folder.get('id'),
                type=folder.get('type'),
                name=folder.get('name'),
                path=folder.get('path'),
                last_edited=folder.get('last_edited'),
                created_on=folder.get('created_on'),
                owner_id=folder.get('owner')
            )
            session.add(folder_obj)
            session.commit()

class DB:
    def __init__(self, conn_link: str):
        self.Session = None
        self.engine = None
        self.session = None
        
        self.user_manager = None
        self.note_manager = None
        self.folder_manager = None
        
        self.conn_link = conn_link

    @contextmanager
    def open_session(self):
        session = self.session
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

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
        with self.open_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user is not None


    def get_item(self, request: Request, id: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))

        with self.open_session() as session:
            note = session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()

            if note is not None:
                return json.dumps({
                    'id': note.id,
                    'type': note.type,
                    'name': note.name,
                    'path': note.path,
                    'last_edited': str(note.last_edited),
                    'created_on': str(note.created_on),
                    'owner_id': note.owner_id,
                    'blocks': note.blocks
                })

            folder = session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).first()

            if folder is not None:
                return json.dumps({
                    'id': folder.id,
                    'name': folder.name,
                    'path': folder.path,
                    'last_edited': str(folder.last_edited),
                    'created_on': str(folder.created_on),
                    'owner_id': folder.owner_id,
                })

            return False


    def delete_item_by_id(self, request: Request, id: str):
        user_id = from_jwt(str(request.cookies.get("authenticate")))

        with self.open_session() as session:
            session.query(Note).filter(Note.path.any(id), Note.owner_id == user_id).delete()
            session.query(Folder).filter(Folder.path.any(id), Folder.owner_id == user_id).delete()

            session.query(Note).filter(Note.id == id, Note.owner_id == user_id).delete()
            session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).delete()
            
            session.commit()


    def update_folder(self, folder: Folder, old_path: list, new_path: list, new_name: str):
        child_items = []
        
        folder.name = new_name
        folder.path = new_path
        folder.last_edited = datetime.now().isoformat()
        
        with self.open_session() as session:
            child_path = old_path + [folder.id]
            child_items = child_items+session.query(Note).filter(Note.path == child_path).all() # Concatenate list NOT append list
            child_items = child_items+session.query(Folder).filter(Folder.path == child_path).all()
            
            for item in child_items:
                if item.type != "folder":
                    item.path = new_path + [folder.id]
                elif item.type == "folder":
                    self.update_folder(item, item.path, (new_path + [folder.id]), item.name)

            session.commit()

    def update_metadata_by_id(self, request: Request, id: str, new_name: str, new_path: list):
        user_id = from_jwt(str(request.cookies.get("authenticate")))
      
        with self.open_session() as session:
            note = session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()
            if note is not None:
                note.name = new_name
                note.path = new_path
                note.last_edited = datetime.now().isoformat()
                session.commit()
                return
            
            folder = session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).first()
            self.update_folder(folder, folder.path, new_path, new_name)


db = DB(os.environ['SQLALCHEMY_URL'])
db.connect()