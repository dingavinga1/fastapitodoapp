from fastapi import APIRouter
from rest.routes.v1.auth import auth_router
from rest.routes.v1.usertodo import usertodo_router

v1_router = APIRouter(prefix = "/api/v1")
v1_router.include_router(auth_router)
v1_router.include_router(usertodo_router)