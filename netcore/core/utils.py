from datetime import timedelta, datetime
from netcore.config import settings
from jose import jwt
from netcore.core.models import UserInDB, User
from typing import Annotated
from fastapi import Security, Depends, status
from fastapi.security import SecurityScopes
from fastapi.exceptions import HTTPException
from netcore.security import oauth2_scheme
from netcore.core.models import TokenData
from pydantic import ValidationError
from jose import JWTError


fake_users_db = [
    {
        "username": "test", 
        "password": "toto", 
        "email": "test@toto.com", 
        "full_name": "Test TOTO", 
        "disabled": False
    }
]


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_user(db, username):
    user = [x for x in db if x.get("username") == username]
    if len(user) == 1:
        return UserInDB(**user[0])


def verify_password(plain_password, password):
    # It's for example, in case you tought it is secure...
    return plain_password == password


def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scopes_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={'WWW-Authenticate': authenticate_value}
            )
    return user

def get_current_active_user(current_user: Annotated[User, Security(get_current_user, scopes=['me'])]):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user