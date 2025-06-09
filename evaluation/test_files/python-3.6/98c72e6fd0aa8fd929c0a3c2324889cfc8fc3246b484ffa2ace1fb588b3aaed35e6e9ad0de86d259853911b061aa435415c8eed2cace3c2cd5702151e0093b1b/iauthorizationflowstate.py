from typing import Any
from typing import Protocol

class IAuthorizationFlowState(Protocol):
    nonce: str
    redirect_uri: str
    state: str

    def is_valid(self, params: Any) -> bool:
        ...