from enum import Enum

class ApiResponse(Enum):
    SUCCESS = 1
    FAILURE = 2
    UNAUTHORIZED = 3

class ClientRole(Enum):
    user = 1
    admin = 100

class IdentityProvider(Enum):
    firebase = 1