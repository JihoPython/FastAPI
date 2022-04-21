from pathlib import Path
import sys

from fastapi import FastAPI

from api import live_router

BASE_DIR = Path(__file__).resolve()
sys.path.append(str(BASE_DIR))

def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(live_router, prefix='/live')
    # app.include_router(static_router, prefix='/static')

    return app

# uvicorn.run(create_app())
app = create_app()