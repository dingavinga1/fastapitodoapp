from enum import Enum
from typing import Any, List, get_type_hints

from bll.repositories.ienvironment import IEnvironmentVariables

class SingletonException(Exception):
    pass

class DependencyExistsException(Exception):
    pass

class DependencyNotExistsException(Exception):
    pass

class DependencyTypes(int, Enum):
    Singleton = 0
    Transient = 1

class DIContainer:
    instances = {}

    @staticmethod
    def get_instance(iface):
        check = DIContainer.instances.get(iface)
        if check is None:
            raise DependencyNotExistsException(str(iface))
        
        impl = check['impl']
        
        if check['type'] == DependencyTypes.Singleton:
            return impl
        
        arg_impls = []
        args = check['args']
        for arg in args:
            get_impl = DIContainer.get_instance(arg)
            arg_impls.append(get_impl)

        return impl(*arg_impls)

    @staticmethod
    def add_instance(iface, dep_type, impl, prereqs):
        if DIContainer.instances.get(iface):
            raise DependencyExistsException()
        
        if dep_type == DependencyTypes.Singleton:
            arg_impls = []
            for arg in prereqs:
                get_impl = DIContainer.get_instance(arg)
                arg_impls.append(get_impl)
            
            i = impl(*arg_impls)
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
