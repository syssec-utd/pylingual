from helios.instrumentation.base import HeliosBaseInstrumentor

class HeliosPsycopg2Instrumentor(HeliosBaseInstrumentor):
    MODULE_NAME = 'opentelemetry.instrumentation.psycopg2'
    INSTRUMENTOR_NAME = 'Psycopg2Instrumentor'

    def __init__(self):
        super().__init__(self.MODULE_NAME, self.INSTRUMENTOR_NAME)

    def instrument(self, tracer_provider=None, **kwargs):
        if self.get_instrumentor():
            self.get_instrumentor().instrument(tracer_provider=tracer_provider, skip_dep_check=True)

    def uninstrument(self):
        super().uninstrument()