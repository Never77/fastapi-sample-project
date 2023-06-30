import strawberry

from netcore.models.users import User


@strawberry.experimental.pydantic.type(model=User, all_fields=True)
class User:
    pass
