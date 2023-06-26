from fastapi import FastAPI
from fastapi_test.config import settings
import logging
from fastapi_test.database import Base, engine
from fastapi_test.routers import UserRouter
import argparse
import uvicorn

# TODO: make it more customizable by .env settings file
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(UserRouter)

@app.get('/')
def home():
    return {'message': "Hello World!"}

@app.get('/info')
def info():
    return settings.dict()

def main():
    parser = argparse.ArgumentParser(description="FastAPI test project")
    parser.add_argument("operation", help="Tells the project what to do", choices=["run"])
    parser.add_argument('--reload', action="store_true", help="Enable hot-reload on saving")
    args = parser.parse_args()

    match(args.operation):
        case "run":
            uvicorn.run(f"{__package__}:app", port=settings.port, reload=args.reload, access_log=settings.access_log, host=settings.host)
        case _:
            raise Exception("Don't know this operation")
