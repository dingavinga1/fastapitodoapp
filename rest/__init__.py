from bll.repositories.iauthentication import IAuthentication
from bll.repositories.ienvironment import IEnvironmentVariables
from bll.repositories.itodo import ITodoRepository
from bll.repositories.iuser import IUserRepository
from bll.services.auth import AuthService
from bll.services.usertodo import UserTodoService
from infra.database import Database
from infra.repositories.environment import DotenvEnvironmentVariables
from infra.repositories.jwt import JWTAuthentication
from infra.repositories.todo import TodoRepository
from infra.repositories.user import UserRepository
from rest.utils.container import DIContainer, DependencyTypes

DIContainer.add_instance(IEnvironmentVariables, DependencyTypes.Transient, DotenvEnvironmentVariables, [])
DIContainer.add_instance(Database, DependencyTypes.Singleton, Database, [IEnvironmentVariables])
DIContainer.add_instance(IUserRepository, DependencyTypes.Transient, UserRepository, [Database])
DIContainer.add_instance(ITodoRepository, DependencyTypes.Transient, TodoRepository, [Database])
DIContainer.add_instance(IAuthentication, DependencyTypes.Transient, JWTAuthentication, [IEnvironmentVariables])
DIContainer.add_instance(AuthService, DependencyTypes.Transient, AuthService, [IUserRepository, IAuthentication, IEnvironmentVariables])
DIContainer.add_instance(UserTodoService, DependencyTypes.Transient, UserTodoService, [ITodoRepository])