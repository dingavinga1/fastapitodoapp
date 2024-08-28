from enum import Enum
from typing import Any, List, TypedDict

class SingletonException(Exception):
    pass

class DependencyExistsException(Exception):
    pass

class DependencyNotExistsException(Exception):
    pass

class DependencyTypes(int, Enum):
    Singleton = 0
    Transient = 1

class PrerequisiteType(int, Enum):
    Interface = 0
    Constant = 1

class Prerequisite(TypedDict):
    type: PrerequisiteType
    keyword: str
    value: Any

class DIContainer:
    instances = {}

    @staticmethod
    def _create_kwargs(prereqs: List[Prerequisite]):
        constructor_arguments = {}
        for req in prereqs:
            if req['type'] == PrerequisiteType.Constant:
                constructor_arguments.update({req['keyword']:req['value']})
            elif req['type'] == PrerequisiteType.Interface:
                constructor_arguments.update({req['keyword']:DIContainer.get_instance(req['value'])})

        return constructor_arguments

    @staticmethod
    def get_instance(iface):
        check = DIContainer.instances.get(iface)
        if check is None:
            raise DependencyNotExistsException(str(iface))
        
        impl = check['impl']
        
        if check['type'] == DependencyTypes.Singleton:
            return impl
        
        kwargs = DIContainer._create_kwargs(check['args'])

        return impl(**kwargs)

    @staticmethod
    def add_instance(iface, dep_type, impl, prereqs: List[PrerequisiteType]):
        if DIContainer.instances.get(iface):
            raise DependencyExistsException()

        if dep_type == DependencyTypes.Singleton:
            kwargs = DIContainer._create_kwargs(prereqs)
            
            i = impl(**kwargs)
            DIContainer.instances[iface] = {
                'type': dep_type,
                'args': prereqs,
                'impl': i
            }
        else:
            DIContainer.instances[iface] = {
                'type': dep_type,
                'args': prereqs,
                'impl': impl
            }            
