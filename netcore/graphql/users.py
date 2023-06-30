import strawberry

from netcore.schemas.users import User


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class User:
    pass
