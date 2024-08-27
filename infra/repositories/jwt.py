from bll.repositories.ienvironment import IEnvironmentVariables
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta

from typing import Any, Dict
from bll.repositories import IAuthentication
from bll.schemas.authschema import AuthClaimsSchema
from bll.schemas.authschema import AuthResponseSchema
from models.exceptions import ExpiredTokenException, InvalidTokenException

class JWTAuthentication(IAuthentication[AuthResponseSchema, AuthClaimsSchema]):
    jwt_algorithm = "HS256"

    def __init__(self, env: IEnvironmentVariables):
        self._env = env

    def create(self, obj: AuthClaimsSchema) -> AuthResponseSchema:
        secret = self._env.get_var("JWT_SECRET")
        expiry = self._env.get_var("JWT_EXPIRY")

        expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=expiry)

        obj_to_encode = obj.model_dump()
        obj_to_encode.update({'exp': expiration_time})

        token = encode(obj_to_encode, secret, algorithm=JWTAuthentication.jwt_algorithm)

        return AuthResponseSchema(
            token=token,
            expiry=int(expiration_time.timestamp())
        )
    
    def verify(self, claims: AuthResponseSchema) -> AuthClaimsSchema:
        secret = self._env.get_var("JWT_SECRET")

        try:
            decoded: Dict[str, Any] = decode(claims.token.encode('utf-8'), secret, algorithms=[JWTAuthentication.jwt_algorithm])
            claim: AuthClaimsSchema = AuthClaimsSchema(**decoded)

            return claim
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except InvalidTokenError:
            raise InvalidTokenException