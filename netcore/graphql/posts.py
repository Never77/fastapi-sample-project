import strawberry
from netcore.models import Post

@strawberry.experimental.pydantic.type(model=Post)
class Post:
    id: str
    content: str