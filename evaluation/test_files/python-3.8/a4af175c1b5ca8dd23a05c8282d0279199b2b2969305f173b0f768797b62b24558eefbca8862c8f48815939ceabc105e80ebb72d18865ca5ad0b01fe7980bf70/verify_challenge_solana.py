import json
from .api_instance import get_api_instance
from openapi_auth.paths.challenge_verify_solana.post import SchemaForRequestBodyApplicationJson

def verify_challenge_solana(api_key: str, body: SchemaForRequestBodyApplicationJson):
    api_instance = get_api_instance(api_key)
    api_response = api_instance.verify_challenge_solana(body=body, accept_content_types='application/json; charset=utf-8', skip_deserialization=True)
    return json.loads(api_response.response.data)