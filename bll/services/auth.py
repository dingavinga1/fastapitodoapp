
from bll.repositories.ienvironment import IEnvironmentVariables
from bll.repositories.iuser import IUserRepository
from bll.schemas.authschema import AuthClaimsSchema, AuthResponseSchema, LoginUserSchema, CreateUserSchema
from bll.repositories.iauthentication import IAuthentication
from bll.utils.auth import AuthHelper
from models.exceptions import AuthenticationFailedException, NotFoundException
from models.user import User

class AuthService:
    def __init__(self, user_repository: IUserRepository, auth_repository: IAuthentication, env: IEnvironmentVariables):
        self._user_repository = user_repository
        self._auth_repository = auth_repository
        self._env = env

    def create(self, user_dto: CreateUserSchema) -> None:
        hashed_pwd = AuthHelper.hash_password(user_dto.password)

        user: User = User(email=user_dto.email, name=user_dto.name, hashed_password=hashed_pwd, is_admin=False)
        
        return self._user_repository.create(user)
    
    def login(self, user_dto: LoginUserSchema) -> AuthResponseSchema:
        try:
            user: User = self._user_repository.get_by_email(user_dto.email)
            auth_result: bool = AuthHelper.verify_password(user_dto.password, user.hashed_password)

            if auth_result is False:
                raise AuthenticationFailedException("Invalid username or password")
            
            auth_check: AuthClaimsSchema = AuthClaimsSchema(id = str(user.id), email = user.email, is_admin = user.is_admin)

            return self._auth_repository.create(auth_check)
        except NotFoundException:
            raise AuthenticationFailedException("Invalid username or password")
