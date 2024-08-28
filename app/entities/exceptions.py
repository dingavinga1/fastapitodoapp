
class AlreadyExistsException(Exception):
    pass

class NotFoundException(Exception):
    pass

class FilterDoesNotExistException(Exception):
    pass

class InvalidTokenException(Exception):
    pass

class ExpiredTokenException(Exception):
    pass

class AuthenticationFailedException(Exception):
    pass