import sys, os
from sqlalchemy import Enum, text, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm.attributes import flag_modified
from starlette_admin.contrib.sqla import Admin, ModelView
from fastapi import FastAPI

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))
from backend.tables import User, Note, Folder

from adminglobalview import AdminGlobalView, Global


Base = declarative_base()
engine = create_engine(os.environ['SQLALCHEMY_URL'])

Base.metadata.create_all(engine)
app = FastAPI()

admin = Admin(engine, title="Tables")

admin.add_view(ModelView(User))
admin.mount_to(app)

admin.add_view(ModelView(Note))
admin.mount_to(app)

admin.add_view(ModelView(Folder))
admin.mount_to(app)

admin.add_view(AdminGlobalView(Global))
admin.mount_to(app)

