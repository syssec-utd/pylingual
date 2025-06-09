from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.reference_document import Statistics, StatisticsSchema

class StatisticsEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + '/statistic'

    def get(self) -> Statistics:
        return self._session.get(self._endpoint).execute().to(StatisticsSchema)