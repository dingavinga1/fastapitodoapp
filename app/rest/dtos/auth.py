from typing import Optional
from pydantic import BaseModel

class SwaggerRequestToken(BaseModel):
    access_token: str
    token_type: str

class LoginUserRequestDto(BaseModel):
    email: str
    password: str

class CreateUserRequestDto(LoginUserRequestDto):
    email: str
    name: str
    password: str

class AuthClaimsDto(BaseModel):
    id: str
    email: str
    is_admin: bool

class LoginResponseDto(BaseModel):
    token: str
    expiry: Optional[int] = None