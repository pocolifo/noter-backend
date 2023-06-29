import json

from sqlalchemy import text, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.attributes import flag_modified 

from datetime import datetime
from starlette.requests import Request

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)

class Folder(Base):
    __tablename__ = 'folders'
    id = Column(Integer, primary_key=True)
    info = Column(JSON)


class DB:
    def __init__(self, conn_link: str):
        self.Session = None
        self.engine = None
        self.session = None
        self.conn_link = conn_link

    def connect(self): # Returns True if connection to database is successful
        try:
            self.engine = create_engine(self.conn_link)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            print(self.session)
            return True
        except Exception:
            return False

        
    def is_authenticated(self, request: Request) -> bool:
        user_id = str(request.cookies.get("authenticate"))
        user = self.session.query(User).filter(text("(users.info->>'id') = :user_id")).params(user_id=user_id).first()
        return user is not None
    
    
    def does_path_exist(self, request: Request, fullpath: list):
        if len(fullpath) == 0: return True

        user_id = str(request.cookies.get("authenticate"))
        folders = self.session.query(Folder).filter(text("(folders.info->'metadata'->'owner'->>'id') = :user_id")).params(user_id=user_id).all()

        for folder in folders:
            if str(folder.info["metadata"]["name"]) == str(fullpath[-1]) and str(folder.info["metadata"]["path"]) == str(fullpath[:-1]):
                return True

        return False

    def get_item(self, request: Request, id: str):
        user_id = str(request.cookies.get("authenticate"))

        note = self.session.query(Note).filter(text("(notes.info->>'id') = :note_id AND (notes.info->'metadata'->'owner'->>'id') = :user_id")).params(note_id=id, user_id=user_id).first()
        
        if note is not None:
            return json.dumps(note.info)

        folder = self.session.query(Folder).filter(text("(folders.info->>'id') = :folder_id AND (folders.info->'metadata'->'owner'->>'id') = :user_id")).params(folder_id=id, user_id=user_id).first()

        if folder is not None:
            return json.dumps(folder.info)

        return False
        

    def get_user_data_by_id(self, id: str):
        user = self.session.query(User).filter(text("(users.info->>'id') = :user_id")).params(user_id=id).first()
        
        if user is not None:
            return json.dumps(user.info)
        
        return False

    def insert_note(self, note: str):
        note_obj = Note(info=json.loads(note))
        self.session.add(note_obj)
        self.session.commit()
    
    def insert_folder(self, folder: str):
        folder_obj = Folder(info=json.loads(folder))
        self.session.add(folder_obj)
        self.session.commit()

    def delete_item_by_id(self, request: Request, id: str):
        user_id = str(request.cookies.get("authenticate"))

        self.session.query(Folder).filter(text("(folders.info->>'id') = :folder_id AND (folders.info->'metadata'->'owner'->>'id') = :user_id")).params(folder_id=id, user_id=user_id).delete()

        self.session.query(Note).filter(text("(notes.info->>'id') = :note_id AND (notes.info->'metadata'->'owner'->>'id') = :user_id")).params(note_id=id, user_id=user_id).delete()

        self.session.commit()

    def update_metadata_by_id(self, request: Request, id: str, new_name: str, new_path: str):
        user_id = str(request.cookies.get("authenticate"))
  
        notes = self.session.query(Note).filter(text("(notes.info->>'id') = :note_id AND (notes.info->'metadata'->'owner'->>'id') = :user_id")).params(note_id=id, user_id=user_id).all()
        folders = self.session.query(Folder).filter(text("(folders.info->>'id') = :folder_id AND (folders.info->'metadata'->'owner'->>'id') = :user_id")).params(folder_id=id, user_id=user_id).all()

        for note in notes:
            note.info['metadata']['name'] = new_name
            note.info['metadata']['path'] = new_path
            note.info['metadata']['lastEdited'] = str(datetime.now().isoformat())
            flag_modified(note, 'info')

        for folder in folders:
            folder.info['metadata']['name'] = new_name
            folder.info['metadata']['path'] = new_path
            folder.info['metadata']['lastEdited'] = str(datetime.now().isoformat())
            flag_modified(folder, 'info')

        self.session.commit()
        
    def update_blocks_by_id(self, request: Request, id: str, new_blocks: str):
        user_id = str(request.cookies.get("authenticate"))

        notes = self.session.query(Note).filter(text("(notes.info->>'id') = :note_id AND (notes.info->'metadata'->'owner'->>'id') = :user_id")).params(note_id=id, user_id=user_id).all()

        for note in notes:
            note.info['blocks'] = new_blocks
            note.info['metadata']['lastEdited'] = datetime.now().isoformat()
            flag_modified(note, 'info')

        self.session.commit()

    def update_lastsignedin(self, request: Request):
        user_id = str(request.cookies.get("authenticate"))

        users = self.session.query(User).filter(text("(users.info->>'id') = :user_id")).params(user_id=user_id).all()

        for user in users:
            user.info['lastSignedIn'] = datetime.now().isoformat()

        self.session.commit()

    def get_users_notes(self, request: Request):
        user_id = str(request.cookies.get("authenticate"))

        notes = self.session.query(Note).filter(text("(notes.info->'metadata'->>'owner'->>'id') = :user_id")).params(user_id=user_id).all()

        return [note.info for note in notes]
    
    def get_users_by_email(self, email: str):
        users = self.session.query(User).filter(text("(users.info->>'email') = :email")).params(email=email).all()

        return [user.info for user in users]
    
    
