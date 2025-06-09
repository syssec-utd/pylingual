from EVECelery.tasks.BaseTasks.ESIResqust import ESIRequest
from EVECelery.exceptions.tasks import InputValidationError

class Route(ESIRequest):

    def get_key(self, origin: int, destination: int):
        return f'Route-{origin}-{destination}'

    def route(self, origin: int, destination: int):
        return f'/route/{origin}/{destination}'

    def validate_inputs(self, origin: int, destination: int):
        try:
            int(origin)
            int(destination)
        except ValueError:
            raise InputValidationError('Input parameter must be an integer.')