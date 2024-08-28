from typing import Optional
from pydantic import BaseModel

class LoginUserRequestModel(BaseModel):
    email: str
    password: str

class CreateUserRequestModel(LoginUserRequestModel):
    email: str
    name: str
    password: str

class AuthClaimsModel(BaseModel):
    id: str
    email: str
    is_admin: bool

class AuthResponseModel(BaseModel):
    token: str
    expiry: Optional[int] = None