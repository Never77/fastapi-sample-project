# FastAPI sample projet

## Installation

You just need to setup a virtualenv and install the package, it will install all needed dependency and let you work when done.

## Development

```bash
pip install -e .[dev]
fastapi-test run --reload
```

## Settings

You can manage settings with ".env" file at the root of the project for example. If you wanna change the filename/path, you can change it in the config.py file.

**_NOTE:_** I need to update the documentation with the list of settings and how it works precisely.

## Structure

I tried to keep the structure as standard as possible. In that way we have some folders with different purpose :

**_NOTE_** Set a tree here to list folders more clearly

* routers 
* models
* schemas
* exceptions
* crud


routers: this folder contains all the code about the API endpoint that will be published by the app. All routers will finally be imported in the main app via include_router function call.

models: this folder contains all code about object to store in database and how to do it.

schemas: this folder contains all object used in the project. They are all based on pydantic BaseModel object to be compliant with the FastAPI core and to be able to serialize them into dict/JSON responses.

exceptions: this folder is quite empty, the goal is to make works a standard way to handle errors in FastAPI by overriding standard handlers per router.

crud: this folder contains all needed code to manipulate object inside the database.

Finally, we have the database.py file that implement the way to connect/use the database itself with sqlalchemy. In this project i used ORM with the Base object created by using declarative_base function. You can change it if needed.

## Next step

Import routers dynamically.

## Features List
- [ ] SSO ([FastAPI-Security](https://jacobsvante.github.io/fastapi-security/))
- [ ] Vault ([Hashicorp Vault](https://www.vaultproject.io))
- [ ] SSOT ([Nautobot](https://github.com/nautobot/nautobot))
- [x] Cache ([Redis](https://redis.io))
- [ ] Document Oriented Database ([MongoDB](https://www.mongodb.com))
- [ ] Monitoring ([Centreon](https://www.centreon.com/fr/))
- [ ] Orchestration ([Luigi](https://luigi.readthedocs.io/en/stable/)/[Prefect](https://www.prefect.io))
- [x] Relational Database ([MySQL](https://www.mysql.com/fr/)/[PostgreSQL](https://www.postgresql.org)/[SQLite](https://www.sqlite.org/index.html))
- [x] GraphQL ([Strawberry](https://strawberry.rocks/docs/integrations/fastapi))
- [x] Asynchronous request handling ([FastAPI Documentation](https://fastapi.tiangolo.com/async/))
- [ ] Containerized ([Docker](https://www.docker.com))
- [ ] Health check endpoint ([e.g: FastAPI Health](https://github.com/Kludex/fastapi-health))
- [ ] TBD ?