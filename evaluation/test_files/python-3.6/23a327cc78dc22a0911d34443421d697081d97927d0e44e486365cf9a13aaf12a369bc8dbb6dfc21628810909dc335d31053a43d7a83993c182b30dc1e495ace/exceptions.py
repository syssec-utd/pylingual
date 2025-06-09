from __future__ import annotations
from airflow.exceptions import AirflowException

class EcsTaskFailToStart(Exception):
    """Raise when ECS tasks fail to start AFTER processing the request."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __reduce__(self):
        return (EcsTaskFailToStart, self.message)

class EcsOperatorError(Exception):
    """Raise when ECS cannot handle the request."""

    def __init__(self, failures: list, message: str):
        self.failures = failures
        self.message = message
        super().__init__(message)

    def __reduce__(self):
        return (EcsOperatorError, (self.failures, self.message))

class S3HookUriParseFailure(AirflowException):
    """When parse_s3_url fails to parse URL, this error is thrown."""