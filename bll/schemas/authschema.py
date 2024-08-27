from typing import Optional
from pydantic import BaseModel

class LoginUserSchema(BaseModel):
    email: str
    password: str

class CreateUserSchema(LoginUserSchema):
    email: str
    name: str
    password: str

class AuthClaimsSchema(BaseModel):
    id: str
    email: str
    is_admin: bool

class AuthResponseSchema(BaseModel):
    token: str
    expiry: Optional[int] = None