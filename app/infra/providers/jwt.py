from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta

from typing import Any, Dict
from usecases.contracts import IAuthentication
from usecases.models.auth import AuthClaimsModel, AuthResponseModel
from entities.exceptions import ExpiredTokenException, InvalidTokenException

class JWTAuthentication(IAuthentication[AuthResponseModel, AuthClaimsModel]):
    jwt_algorithm = "HS256"

    def __init__(self, secret, expiry):
        self._secret = secret
        self._expiry = expiry

    def create(self, obj: AuthClaimsModel) -> AuthResponseModel:
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=self._expiry)

        obj_to_encode = obj.model_dump()
        obj_to_encode.update({'exp': expiration_time})

        token = encode(obj_to_encode, self._secret, algorithm=JWTAuthentication.jwt_algorithm)

        return AuthResponseModel(
            token=token,
            expiry=int(expiration_time.timestamp())
        )
    
    def verify(self, claims: AuthResponseModel) -> AuthClaimsModel:
        try:
            decoded: Dict[str, Any] = decode(claims.token.encode('utf-8'), self._secret, algorithms=[JWTAuthentication.jwt_algorithm])
            claim: AuthClaimsModel = AuthClaimsModel(**decoded)

            return claim
        except ExpiredSignatureError:
            raise ExpiredTokenException
        except InvalidTokenError:
            raise InvalidTokenException