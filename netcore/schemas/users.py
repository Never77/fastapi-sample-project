from uuid import uuid4

from sqlalchemy import Boolean, Column, String
from sqlalchemy_utils import EmailType, UUIDType

from netcore.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUIDType, unique=True, primary_key=True, nullable=False, default=uuid4)
    email = Column(EmailType, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
