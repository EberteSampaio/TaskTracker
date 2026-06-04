class DomainException(Exception):
    pass

class CommandNotFoundException(DomainException):
    pass

class TaskNotFoundException(DomainException):
    pass
