from fastapi import APIRouter, Request
from netcore.security.sso import gaap
import json

router = APIRouter(prefix='/auth', tags=["auth"])

@router.get('/info')
async def info(request: Request):
    return request.session.get('user')

@router.get('/login/sso')
async def login_via_sso(request: Request):
    redirect_uri = request.url_for('authorize_gaap')  # the function below
    return await gaap.authorize_redirect(request, redirect_uri)

@router.post('/login/gaap')  # callback URL -> Need to be authorized by the auth side as a callback url
async def authorize_gaap(request: Request):
    token = await gaap.authorize_access_token(request)
    # do something with the token and userinfo
    return token['userinfo']  # Need to test this route with a DNS resolved server