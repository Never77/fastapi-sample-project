import strawberry

from netcore.models.secrets import Account

@strawberry.experimental.pydantic.type(model=Account, all_fields=True)
class Account:
    pass