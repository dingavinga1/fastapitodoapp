from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from rest.dtos.auth import LoginUserRequestDto, LoginResponseDto, CreateUserRequestDto
from usecases.models.auth import AuthResponseModel, CreateUserRequestModel, LoginUserRequestModel
from usecases.services.auth import AuthService
from rest.dtos.auth import SwaggerRequestToken
from configs.container import DIContainer

auth_router = APIRouter(prefix="/auth")

@auth_router.post('/login', response_model=LoginResponseDto)
def login(login_dto: LoginUserRequestDto, auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))) -> LoginResponseDto:
    login_model: LoginUserRequestModel = LoginUserRequestModel(email=login_dto.email, password=login_dto.password)
    response: AuthResponseModel = auth_service.login(login_model)
    return LoginResponseDto(token=response.token, expiry=response.expiry)

@auth_router.post('/', status_code=201)
def signup(create_dto: CreateUserRequestDto, auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))):
    signup_model: CreateUserRequestModel = CreateUserRequestModel(email=create_dto.email, password=create_dto.password, name=create_dto.name)
    return auth_service.signup(signup_model)

@auth_router.post('/token')
def swagger_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthService = Depends(lambda: DIContainer.get_instance(AuthService))) -> SwaggerRequestToken:
    req = LoginUserRequestModel(email = form_data.username, password = form_data.password)
    
    auth_response: AuthResponseModel = auth_service.login(req)

    return SwaggerRequestToken(access_token=auth_response.token, token_type="bearer")