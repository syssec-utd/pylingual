class BaseError(Exception):
    """
    Base package error.
    """

class ModelError(BaseError):
    """
    Model definition error.
    """

class ModelFieldError(BaseError):
    """
    Model field definition error.
    """

    def __init__(self, model_name: str, field_name: str, message: str):
        self.model_name = model_name
        self.field_name = field_name
        self.message = message
        super().__init__(f'{model_name}.{field_name} field type incorrect: {message}')

class ParsingError(BaseError):
    """
    Xml parsing error.
    """