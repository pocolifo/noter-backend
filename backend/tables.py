from sqlalchemy import Enum, text, TEXT, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# NOTE: as_uuid=True will make `id` be of type uuid.UUID, which FastAPI cannot serialize.
#       as_uuid=False will return it as a string (which is all we really need anyway) and
#       not cause serialization issues.

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=False), primary_key=True)
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

    id = Column(UUID(as_uuid=False), primary_key=True)
    type = Column(String)
    name = Column(String)
    path = Column(ARRAY(String))
    last_edited = Column(String)
    created_on = Column(String)
    owner_id = Column(UUID(as_uuid=False), ForeignKey('users.id'))
    blocks = Column(JSON)

    owner = relationship("User", back_populates="notes")


class Folder(Base):
    __tablename__ = 'folders'
    
    id = Column(UUID(as_uuid=False), primary_key=True)
    type = Column(String)
    name = Column(String)
    path = Column(ARRAY(String))
    last_edited = Column(String)
    created_on = Column(String)
    owner_id = Column(UUID(as_uuid=False), ForeignKey('users.id'))

    owner = relationship("User")