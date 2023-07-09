from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from netcore.security.sso import gaap
from typing import Annotated
from netcore.core import utils, models
from fastapi.exceptions import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])


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


@router.post("/login", response_model=models.Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Here will need to authenticate with the LDAP backend for example or another auth service using the values sent by the user in the form.
    """
    user = utils.authenticate_user(utils.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = utils.create_access_token(
        data= {"sub": user.username, "scopes": form_data.scopes},
    )
    # Need to store it in the session in the front-end
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=models.User)
async def read_users_me(current_user: Annotated[models.User, Depends(utils.get_current_active_user)]):
    """
    To avoid any confustion, it's just for demonstration purpose to prove that the concept works, obviously to provide a token you'll need to be authenticated.
    """
    return current_user

@router.get('/status')
async def read_system_status(current_user: Annotated[models.User, Depends(utils.get_current_user)]):
    return {"status": "ok"}
