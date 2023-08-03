import sys, os
from sqlalchemy import Enum, text, Column, Integer, String, ARRAY, JSON, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm.attributes import flag_modified
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))

# Add environment variables in .env
from backend.tables import User, Note, Folder

from app.views import HomeView, AccessFlagsView


engine = create_engine(os.environ['SQLALCHEMY_URL'])
app = Starlette()
app.state.session = sessionmaker(engine)

admin = Admin(engine, title="Tables", base_url='/')

admin.add_view(HomeView('Home'))
admin.add_view(AccessFlagsView('Access Flags', path='/access-flags', methods=['GET', 'POST']))
admin.add_view(ModelView(User))
admin.add_view(ModelView(Note))
admin.add_view(ModelView(Folder))
admin.mount_to(app)
