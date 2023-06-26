from fastapi_test.database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy_utils import UUIDType, EmailType
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(UUIDType, unique=True, primary_key=True, nullable=False, default=uuid4)
    email = Column(EmailType, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)