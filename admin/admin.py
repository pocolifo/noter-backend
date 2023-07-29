import sys, os
from sqlalchemy import Enum, text, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm.attributes import flag_modified
from starlette_admin.contrib.sqla import Admin, ModelView
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from backend.tables import User, Note, Folder

Base = declarative_base()
engine = create_engine("postgresql://postgres:ilovebigblackcock69@localhost/postgres2")

Base.metadata.create_all(engine)
app = FastAPI()

admin = Admin(engine, title="Tables")

admin.add_view(ModelView(User))
admin.mount_to(app)

admin.add_view(ModelView(Note))
admin.mount_to(app)

admin.add_view(ModelView(Folder))
admin.mount_to(app)


"""
class BaseManager:
    def __init__(self, session):
        self.session = session

class Administrator:
    def __init__(self, conn_link:str):
        self.Session = None
        self.engine = None
        self.session = None
        
        self.item_admin = None
        self.user_admin = None
        
        self.conn_link = conn_link
        
    def connect(self):
        try:
            self.engine = create_engine(self.conn_link)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            
            self.item_admin = ItemAdmin(self.session)
            self.user_admin = UserAdmin(self.session)
            return True
            
        except Exception:
            return False
"""
    