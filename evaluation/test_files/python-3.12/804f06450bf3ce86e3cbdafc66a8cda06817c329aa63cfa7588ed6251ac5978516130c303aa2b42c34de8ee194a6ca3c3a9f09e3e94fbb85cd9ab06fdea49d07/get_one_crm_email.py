import dataclasses
from typing import Optional
from dataclasses_json import dataclass_json
from vesselapi import utils
from ..shared import email as shared_email

@dataclasses.dataclass
class GetOneCrmEmailQueryParams:
    access_token: str = dataclasses.field(metadata={'query_param': {'field_name': 'accessToken', 'style': 'form', 'explode': True}})
    id: str = dataclasses.field(metadata={'query_param': {'field_name': 'id', 'style': 'form', 'explode': True}})
    all_fields: Optional[bool] = dataclasses.field(default=None, metadata={'query_param': {'field_name': 'allFields', 'style': 'form', 'explode': True}})

@dataclass_json
@dataclasses.dataclass
class GetOneCrmEmailResponseBody:
    email: Optional[shared_email.Email] = dataclasses.field(default=None, metadata={'dataclasses_json': {'letter_case': utils.field_name('email')}})

@dataclasses.dataclass
class GetOneCrmEmailRequest:
    query_params: GetOneCrmEmailQueryParams = dataclasses.field()

@dataclasses.dataclass
class GetOneCrmEmailResponse:
    content_type: str = dataclasses.field()
    status_code: int = dataclasses.field()
    response_body: Optional[GetOneCrmEmailResponseBody] = dataclasses.field(default=None)