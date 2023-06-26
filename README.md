# FastAPI sample projet

## Development

```bash
pip install -e .[dev]
fastapi-test run
```

## Settings

You can manage settings with ".env" file at the root of the project for example. If you wanna change the filename/path, you can change it in the config.py file.

## Structure

I tried to keep the structure as standard as possible. In that way we have some folders with different purpose :
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