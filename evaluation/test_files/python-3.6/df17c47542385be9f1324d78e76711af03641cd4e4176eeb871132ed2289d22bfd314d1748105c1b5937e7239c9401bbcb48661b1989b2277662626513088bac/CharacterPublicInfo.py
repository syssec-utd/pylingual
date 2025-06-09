from EVECelery.tasks.BaseTasks.ESIResqust import ESIRequest
from EVECelery.exceptions.tasks import InputValidationError

class CharacterPublicInfo(ESIRequest):

    def ttl_404(self) -> int:
        return 86400

    def get_key(self, character_id: int):
        return f'CharacterPublicInfo-{character_id}'

    def route(self, character_id: int):
        return f'/characters/{character_id}'

    def validate_inputs(self, character_id: int) -> None:
        try:
            int(character_id)
        except ValueError:
            raise InputValidationError('Input parameter must be an integer.')