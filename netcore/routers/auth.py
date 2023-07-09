from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from netcore.security.sso import gaap

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # No need to set the / at the beginning


@router.get("/info")
async def info(request: Request):
    return request.session.get("user")


@router.get("/login/sso")
async def login_via_sso(request: Request):
    redirect_uri = request.url_for("authorize_gaap")  # the function below
    return await gaap.authorize_redirect(request, redirect_uri)


@router.post("/login/gaap")  # callback URL -> Need to be authorized by the auth side as a callback url
async def authorize_gaap(request: Request):
    token = await gaap.authorize_access_token(request)
    # do something with the token and userinfo
    return token["userinfo"]  # Need to test this route with a DNS resolved server


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Here will need to authenticate with the LDAP backend for example or another auth service using the values sent by the user in the form.
    """
    return {"access_token": form_data.username, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """
    To avoid any confustion, it's just for demonstration purpose to prove that the concept works, obviously to provide a token you'll need to be authenticated.
    """
    return token
