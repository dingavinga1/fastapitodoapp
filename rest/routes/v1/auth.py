from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from bll.schemas.authschema import AuthResponseSchema, CreateUserSchema, LoginUserSchema
from bll.services.auth import AuthService
from rest.utils.auth import SwaggerRequestToken
from rest.utils.container import DIContainer

auth_router = APIRouter(prefix="/auth")

@auth_router.post('/login', response_model=AuthResponseSchema)
def login(login_dto: LoginUserSchema, auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))) -> AuthResponseSchema:
    return auth_service.login(login_dto)

@auth_router.post('/', status_code=201)
def create(create_dto: CreateUserSchema, auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))):
    return auth_service.create(create_dto)

@auth_router.post('/token')
def swagger_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))) -> SwaggerRequestToken:
    req = LoginUserSchema(email = form_data.username, password = form_data.password)
    
    auth_response = auth_service.login(req)

    return SwaggerRequestToken(access_token=auth_response.token, token_type="bearer")