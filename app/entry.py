from typing import List
from configs.container import DIContainer, Prerequisite, PrerequisiteType, DependencyTypes
from infra.database import Database
from infra.providers.environment import DotenvEnvironmentVariables
from infra.providers.jwt import JWTAuthentication
from infra.repositories.todo import TodoRepository
from infra.repositories.user import UserRepository
from usecases.contracts.iauthentication import IAuthentication
from configs.ienvironment import IEnvironmentVariables
from usecases.contracts.itodo import ITodoRepository
from usecases.contracts.iuser import IUserRepository
from usecases.services.auth import AuthService
from usecases.services.usertodo import UserTodoService

def configure_environment():
    prereqs = []
    DIContainer.add_instance(IEnvironmentVariables, DependencyTypes.Transient, DotenvEnvironmentVariables, [])

def configure_database():
    env: IEnvironmentVariables = DIContainer.get_instance(IEnvironmentVariables)

    prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'host',
            'value': env.get_var('DB_HOST')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'port',
            'value': env.get_var('DB_PORT')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'name',
            'value': env.get_var('DB_NAME')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'user',
            'value': env.get_var('DB_USER')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'password',
            'value': env.get_var('DB_PASS')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'debug_mode',
            'value': env.get_var('DEBUG_MODE')
        }
    ]
    
    DIContainer.add_instance(Database, DependencyTypes.Singleton, Database, prereqs)

def configure_repositories():
    user_prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Interface,
            'keyword': 'db',
            'value': Database
        }
    ]

    auth_prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Interface,
            'keyword': 'db',
            'value': Database
        }
    ]

    DIContainer.add_instance(IUserRepository, DependencyTypes.Transient, UserRepository, user_prereqs)
    DIContainer.add_instance(ITodoRepository, DependencyTypes.Transient, TodoRepository, auth_prereqs)

def configure_jwt():
    env: IEnvironmentVariables = DIContainer.get_instance(IEnvironmentVariables)

    prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'secret',
            'value': env.get_var('JWT_SECRET')
        },
        {
            'type': PrerequisiteType.Constant,
            'keyword': 'expiry',
            'value': env.get_var('JWT_EXPIRY')
        }
    ]

    DIContainer.add_instance(IAuthentication, DependencyTypes.Transient, JWTAuthentication, prereqs)

def configure_services():
    auth_prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Interface,
            'keyword': 'user_repository',
            'value': IUserRepository
        },
        {
            'type': PrerequisiteType.Interface,
            'keyword': 'authentication',
            'value': IAuthentication
        }
    ]

    todo_prereqs: List[Prerequisite] = [
        {
            'type': PrerequisiteType.Interface,
            'keyword': 'todo_repository',
            'value': ITodoRepository
        }
    ]

    DIContainer.add_instance(AuthService, DependencyTypes.Transient, AuthService, auth_prereqs)
    DIContainer.add_instance(UserTodoService, DependencyTypes.Transient, UserTodoService, todo_prereqs)

def inject_dependencies():
    configure_environment()
    configure_database()
    configure_repositories()
    configure_jwt()
    configure_services()

inject_dependencies()

from rest.app import app