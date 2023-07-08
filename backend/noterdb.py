import json

from sqlalchemy import text, Column, Integer, String, ARRAY, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.orm.attributes import flag_modified 

from datetime import datetime
from starlette.requests import Request

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    primary_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    stripe_id = Column(String)
    lastSignedIn = Column(String)
    joinedOn = Column(String)
    history = Column(JSON)
    notes = relationship("Note", back_populates="owner")

class Note(Base):
    __tablename__ = 'notes'

    primary_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    type = Column(String)
    name = Column(String)
    path = Column(ARRAY(String))
    lastEdited = Column(String)
    createdOn = Column(String)
    owner_id = Column(String, ForeignKey('users.id'))
    blocks = Column(JSON)

    owner = relationship("User", back_populates="notes")

class Folder(Base):
    __tablename__ = 'folders'
    
    primary_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    type = Column(String)
    name = Column(String)
    path = Column(ARRAY(String))
    lastEdited = Column(String)
    createdOn = Column(String)
    owner_id = Column(String, ForeignKey('users.id'))

    owner = relationship("User")


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
            return True
        except Exception:
            return False

        
    def is_authenticated(self, request: Request) -> bool:
        user_id = str(request.cookies.get("authenticate"))
        user = self.session.query(User).filter(User.id == user_id).first()
        return user is not None
    
    
    def does_path_exist(self, request: Request, fullpath: list):
        if len(fullpath) == 0: 
            return True

        user_id = str(request.cookies.get("authenticate"))
        folders = self.session.query(Folder).filter(Folder.owner_id == user_id).all()

        for folder in folders:
            if folder.name == fullpath[-1] and folder.path == fullpath[:-1]:
                return True

        return False

    def get_item(self, request: Request, id: str):
        user_id = str(request.cookies.get("authenticate"))

        note = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).first()

        if note is not None:
            return json.dumps({
                'id': note.id,
                'type': note.type,
                'name': note.name,
                'path': note.path,
                'lastEdited': note.lastEdited,
                'createdOn': note.createdOn,
                'owner_id': note.owner_id,
                'blocks': note.blocks
            })

        folder = self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).first()

        if folder is not None:
            return json.dumps({
                'id': folder.id,
                'type': folder.type,
                'name': folder.name,
                'path': folder.path,
                'lastEdited': folder.lastEdited,
                'createdOn': folder.createdOn,
                'owner_id': folder.owner_id,
            })

        return False

        

    def get_user_data_by_id(self, id: str):
        user = self.session.query(User).filter(User.id == id).first()
            
        if user is not None:
            return json.dumps({
                'id': user.id,
                'email': user.email,
                'password': user.password,
                'stripe_id': user.stripe_id,
                'lastSignedIn': user.lastSignedIn,
                'joinedOn': user.joinedOn,
                'history': user.history,
            })
            
        return False

    def insert_user(self, user: dict):
        user_obj = User(
            id=user.get('id'),
            email=user.get('email'),
            password=user.get('password'),
            stripe_id=user.get('stripe_id'),
            lastSignedIn=user.get('lastSignedIn'),
            joinedOn=user.get('joinedOn'),
            
            history=user.get('history')
        )
        self.session.add(user_obj)
        self.session.commit()


    def insert_note(self, note: dict):
        note_obj = Note(
            id=note.get('id'),
            type=note.get('type'),
            name=note.get('name'),
            path=note.get('path'),
            lastEdited=note.get('lastEdited'),
            createdOn=note.get('createdOn'),
            owner_id=note.get('owner'),
            blocks=note.get('blocks')
        )
        self.session.add(note_obj)
        self.session.commit()

    
    def insert_folder(self, folder: dict):
        folder_obj = Folder(
            id=folder.get('id'),
            type=folder.get('type'),
            name=folder.get('name'),
            path=folder.get('path'),
            lastEdited=folder.get('lastEdited'),
            createdOn=folder.get('createdOn'),
            owner_id=folder.get('owner')
        )
        self.session.add(folder_obj)
        self.session.commit()


    def delete_item_by_id(self, request: Request, id: str):
        user_id = str(request.cookies.get("authenticate"))

        self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).delete()
        self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).delete()
        
        self.session.commit()


    def update_metadata_by_id(self, request: Request, id: str, new_name: str, new_path: str):
        user_id = str(request.cookies.get("authenticate"))
      
        notes = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).all()
        folders = self.session.query(Folder).filter(Folder.id == id, Folder.owner_id == user_id).all()

        for note in notes:
            note.name = new_name
            note.path = json.loads(new_path)
            note.lastEdited = datetime.now().isoformat()

        for folder in folders:
            folder.name = new_name
            folder.path = json.loads(new_path)
            folder.lastEdited = datetime.now().isoformat()

        self.session.commit()

        
    def update_blocks_by_id(self, request: Request, id: str, new_blocks: str):
        user_id = str(request.cookies.get("authenticate"))

        notes = self.session.query(Note).filter(Note.id == id, Note.owner_id == user_id).all()

        for note in notes:
            note.blocks = json.loads(new_blocks)
            note.lastEdited = datetime.now().isoformat()

        self.session.commit()


    def update_lastsignedin(self, request: Request):
        user_id = str(request.cookies.get("authenticate"))

        users = self.session.query(User).filter(User.id == user_id).all()

        for user in users:
            user.lastSignedIn = datetime.now().isoformat()

        self.session.commit()

    def get_users_notes(self, request: Request):
        user_id = str(request.cookies.get("authenticate"))
        notes = self.session.query(Note).filter(Note.owner_id == user_id).all()
        return [{"id": note.id, "type": note.type, "name": note.name, "path": note.path, "lastEdited": note.lastEdited, "createdOn": note.createdOn, "blocks": note.blocks} for note in notes]

    
    def get_users_by_email(self, email: str):
        users = self.session.query(User).filter(User.email == email).all()
        return [{"id": user.id, "email": user.email, "password": user.password, "stripe_id": user.stripe_id, "lastSignedIn": user.lastSignedIn, "joinedOn": user.joinedOn, "history": user.history} for user in users]
        
        
    
        
        
