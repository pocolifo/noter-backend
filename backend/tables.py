from sqlalchemy import Enum, text, TEXT, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    primary_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    email = Column(String)
    name = Column(String)
    pfp = Column(TEXT)
    password = Column(String)
    stripe_id = Column(String)
    last_signed_in = Column(String)
    joined_on = Column(String)
    history = Column(JSON)
    email_verified = Column(Boolean)
    has_noter_access = Column(Boolean)
    verification_code = Column(String)
    
    notes = relationship("Note", back_populates="owner")


class Note(Base):
    __tablename__ = 'notes'

    primary_id = Column(Integer, primary_key=True)
    id = Column(String, unique=True)
    type = Column(String)
    name = Column(String)
    path = Column(ARRAY(String))
    last_edited = Column(String)
    created_on = Column(String)
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
    last_edited = Column(String)
    created_on = Column(String)
    owner_id = Column(String, ForeignKey('users.id'))

    owner = relationship("User")