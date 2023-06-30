import strawberry
from netcore.models.hosts import Host

@strawberry.experimental.pydantic.type(model=Host, all_fields=True)
class Host:
    pass