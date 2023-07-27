# Bootstraps the app

import uvicorn
from backend.app import app_init

uvicorn.run(app=app_init())