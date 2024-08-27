from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from bll.repositories.iauthentication import IAuthentication
from bll.schemas.authschema import AuthClaimsSchema, AuthResponseSchema
from rest.utils.container import DIContainer

class SwaggerRequestToken(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

def get_active_user(token: Annotated[str, Depends(oauth2_scheme)], auth_repository: IAuthentication = Depends(lambda: DIContainer.get_instance(IAuthentication))) -> AuthClaimsSchema:
    dto: AuthResponseSchema = AuthResponseSchema(token = token)
    claims: AuthClaimsSchema = auth_repository.verify(dto)

    return claims