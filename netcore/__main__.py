import argparse
import logging

import uvicorn
from fastapi import FastAPI
from fastapi_redis_cache import FastApiRedisCache
from prometheus_fastapi_instrumentator import Instrumentator

from netcore.config import settings
from netcore.database import Base, engine

if settings.graphql:
    from strawberry import Schema
    from strawberry.fastapi import GraphQLRouter

    from netcore.graphql import Query

if settings.vault.url:
    from netcore.routers import SecretsRouter

if settings.nautobot.url:
    from netcore.routers import HostsRouter

import importlib.metadata

from netcore.routers import UserRouter

# TODO: make it more customizable by .env settings file
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    datefmt="%d/%m/%Y %H:%M:%S",
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

print(settings)

app = FastAPI(title="NetCore", version=importlib.metadata.version(__package__ or __name__))
app.include_router(UserRouter)
if settings.graphql:
    app.include_router(GraphQLRouter(Schema(Query)), prefix="/graphql")

if settings.vault.url:
    app.include_router(SecretsRouter)

if settings.nautobot.url:
    app.include_router(HostsRouter)

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
    parser = argparse.ArgumentParser(description="NetCore")
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
