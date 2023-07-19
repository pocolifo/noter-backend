from sqlalchemy import Enum, text, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.orm.attributes import flag_modified



class BaseManager:
    def __init__(self, session):
        self.session = session


class ItemAdmin(BaseManager):
    # NEXT COMMIT



class UserAdmin(BaseManager):
    # NEXT COMMIT

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
            
    