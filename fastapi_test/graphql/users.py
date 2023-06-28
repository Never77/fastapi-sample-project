import strawberry

from fastapi_test.schemas.users import User


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class User:
    pass
