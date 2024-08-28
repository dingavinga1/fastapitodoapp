from fastapi import FastAPI
from rest.middlewares.exceptions import ExceptionHandlingMiddleware
from rest.routes.v1 import v1_router

app = FastAPI()

app.add_middleware(ExceptionHandlingMiddleware)

app.include_router(v1_router)