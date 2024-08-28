from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from entities.exceptions import *

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except AlreadyExistsException:
            return JSONResponse(content={"detail": "Record already exists"}, status_code=422)
        except NotFoundException:
            return JSONResponse(content={"detail": "Record not found"}, status_code=404)
        except FilterDoesNotExistException:
            return JSONResponse(content={"detail": "Invalid filter"}, status_code=422)
        except InvalidTokenException:
            return JSONResponse(content={"detail": "Invalid/Expired Token"}, status=401)
        except ExpiredTokenException:
            return JSONResponse(content={"detail": "Invalid/Expired Token"}, status=401)
        except AuthenticationFailedException:
            return JSONResponse(content={"detail": "Invalid email/password"}, status_code=401)
        except Exception as e:
            print(e)
            return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)