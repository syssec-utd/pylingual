"""
Module which have all our exceptions
"""

class PKCS11TimeoutException(Exception):
    """Class to handle PKCS11 timeout exceptions"""

    def __init__(self, message: str='PKCS11 timeout exceeded') -> None:
        self.message = message
        super().__init__(self.message)

class PKCS11UnknownErrorException(Exception):
    """Class to handle PKCS11 exceptions"""

    def __init__(self, message: str='PKCS11 Exception happened') -> None:
        self.message = message
        super().__init__(self.message)

class DuplicateExtensionException(Exception):
    """Class to handle PKCS11 timeout exceptions"""

    def __init__(self, message: str='Duplicate extension not allowed') -> None:
        self.message = message
        super().__init__(self.message)