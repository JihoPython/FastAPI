from pathlib import Path
import sys

from fastapi import FastAPI
import uvicorn

from api import live_router

BASE_DIR = Path(__file__).resolve()
sys.path.append(str(BASE_DIR))

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(live_router, prefix='/live')

    return app

uvicorn.run(create_app())