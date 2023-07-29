# Bootstraps the app

import uvicorn
from backend.app import app_init
from backend.environment import load_all, append_to_environ

append_to_environ(load_all())
uvicorn.run(app=app_init())