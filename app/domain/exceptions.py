class DomainException(Exception):
    pass


class UserNotFound(DomainException):
    pass


class EmailAlreadyExists(DomainException):
    pass


class InsufficientFunds(DomainException):
    pass


class InvalidTransfer(DomainException):
    pass