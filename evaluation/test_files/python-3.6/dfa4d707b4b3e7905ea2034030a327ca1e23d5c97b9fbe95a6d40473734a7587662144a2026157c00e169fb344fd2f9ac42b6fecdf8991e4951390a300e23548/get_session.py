from dataclasses import dataclass
from typing import Optional
from atproto.xrpc_client.models import base

@dataclass
class Response(base.ResponseModelBase):
    """Output data model for :obj:`com.atproto.server.getSession`.

    Attributes:
        handle: Handle.
        did: Did.
        email: Email.
    """
    did: str
    handle: str
    email: Optional[str] = None