
from usecases.contracts.iuser import IUserRepository
from usecases.models.auth import AuthClaimsModel, AuthResponseModel, LoginUserRequestModel, CreateUserRequestModel
from usecases.contracts.iauthentication import IAuthentication
from entities.exceptions import AuthenticationFailedException, NotFoundException
from entities.user import UserEntity
import bcrypt

class AuthService:
    def __init__(self, user_repository: IUserRepository, authentication: IAuthentication):
        self._user_repository = user_repository
        self._authentication = authentication

    def _hash_password(self, password: str) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_pwd.decode('utf-8')
    
    def _verify_password(self, plain: str, hashed: str) -> bool:
        pwd_bytes = plain.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)

    def signup(self, user_dto: CreateUserRequestModel) -> None:
        hashed_pwd = self._hash_password(user_dto.password)

        user: UserEntity = UserEntity(email=user_dto.email, name=user_dto.name, hashed_password=hashed_pwd, is_admin=False)
        
        return self._user_repository.create(user)
    
    def login(self, user_dto: LoginUserRequestModel) -> AuthResponseModel:
        try:
            user: UserEntity = self._user_repository.get_by_email(user_dto.email)
            auth_result: bool = self._verify_password(user_dto.password, user.hashed_password)

            if auth_result is False:
                raise AuthenticationFailedException("Invalid username or password")
            
            auth_check: AuthClaimsModel = AuthClaimsModel(id = str(user.id), email = user.email, is_admin = user.is_admin)

            return self._authentication.create(auth_check)
        except NotFoundException:
            raise AuthenticationFailedException("Invalid username or password")
