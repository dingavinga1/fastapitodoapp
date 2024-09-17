from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from configs.container import DIContainer
from usecases.contracts.iauthentication import IAuthentication
from usecases.models.auth import AuthClaimsModel, AuthResponseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

def get_active_user(request: Request, token: Annotated[str, Depends(oauth2_scheme)], auth_provider: IAuthentication = Depends(lambda: DIContainer.get_instance(IAuthentication))) -> AuthClaimsModel:
    dto: AuthResponseModel = AuthResponseModel(token = token)
    claims: AuthClaimsModel = auth_provider.verify(dto)

    request.state.auth_context = claims
    return claims