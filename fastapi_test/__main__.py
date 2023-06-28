import argparse
import logging

import uvicorn
from fastapi import FastAPI
from fastapi_redis_cache import FastApiRedisCache
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi_test.config import settings
from fastapi_test.database import Base, engine

if settings.graphql:
    from strawberry import Schema
    from strawberry.fastapi import GraphQLRouter
    from fastapi_test.graphql import Query

from fastapi_test.routers import UserRouter

# TODO: make it more customizable by .env settings file
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


app = FastAPI()
app.include_router(UserRouter)
if settings.graphql:
    app.include_router(GraphQLRouter(Schema(Query)), prefix="/graphql")

instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
async def startup():
    if settings.redis_url:
        redis_cache = FastApiRedisCache()
        redis_cache.init(
            host_url=settings.redis_url,
            prefix="FastAPI-Cache",  # Prefix of the keys you want in Redis
            # response_header="X-FastAPI-Cache",  # Header you want to provide when it's cached
            # ignore_arg_types=[Request, Response, Session]
        )
    if settings.prometheus:
        instrumentator.expose(app)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Dev purpose
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def home():
    return {"message": "Hello World!"}


@app.get("/info")
def info():
    return settings.dict()


def main():
    parser = argparse.ArgumentParser(description="FastAPI test project")
    parser.add_argument("operation", help="Tells the project what to do", choices=["run"])
    parser.add_argument("--reload", action="store_true", help="Enable hot-reload on saving")
    args = parser.parse_args()

    match (args.operation):
        case "run":
            uvicorn.run(
                f"{__package__}:app",
                port=settings.port,
                reload=args.reload,
                access_log=settings.access_log,
                host=settings.host,
            )
        case _:
            raise Exception("Don't know this operation")
