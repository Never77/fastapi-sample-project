from netcore.security.sso import oauth
from fastapi.security import OAuth2PasswordBearer

# Absolute path for tokenUrl may cause issues behind a proxy, it is important to keep it relative f we read the doc : https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # No need to set the / at the beginning


__all__ = ("oauth","oauth2_scheme",)
