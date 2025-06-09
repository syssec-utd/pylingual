from typing import TYPE_CHECKING, Tuple
from datetime import datetime, timedelta
from threading import Timer
import logging
if TYPE_CHECKING:
    from weconnect.api.cupra.elements.vehicle import Vehicle
from weconnect.elements.generic_status import GenericStatus
from weconnect.api.cupra.domain import Domain
LOG = logging.getLogger('weconnect')

class RequestTracker:

    def __init__(self, vehicle: 'Vehicle') -> None:
        self.vehicle: 'Vehicle' = vehicle
        self.requests: dict[Domain, list[Tuple[str, datetime, datetime]]] = {}
        self.__timer = None

    def clear(self) -> None:
        self.requests.clear()
        if self.__timer is not None or self.__timer.is_alive():
            self.__timer.cancel()

    def trackRequest(self, id: str, domain: Domain, minTime: int, maxTime: int) -> None:
        minDate = datetime.now() + timedelta(seconds=minTime)
        maxDate = datetime.now() + timedelta(seconds=maxTime)
        LOG.debug('Track requests for id %s in %s at lesat until %s, at most until %s every 5 seconds', id, domain.value, minDate, maxDate)
        if domain not in self.requests:
            self.requests[domain] = [(id, minDate, maxDate)]
        else:
            self.requests[domain].append((id, minDate, maxDate))
        if self.__timer is None or not self.__timer.is_alive():
            self.__timer = Timer(5, self.update)
            self.__timer.daemon = True
            self.__timer.start()

    def update(self) -> None:
        LOG.debug('request tracking update status for %d domains', len(self.requests))
        self.vehicle.updateStatus(force=True, selective=self.requests)
        openRequests = []
        for domain, statuses in self.vehicle.domains.items():
            for status in statuses.values():
                if status.hasRequests():
                    openRequests.extend(status.requests.values())
        for domain, requests in list(self.requests.items()):
            for request in requests:
                id, minDate, maxDate = request
                if maxDate < datetime.now():
                    requests.remove(request)
                    LOG.debug('request tracking for id %s timed out', id)
                elif openRequests:
                    for openRequest in openRequests:
                        if openRequest.requestId.value == id:
                            if openRequest.status.value not in (GenericStatus.Request.Status.IN_PROGRESS, GenericStatus.Request.Status.QUEUED, GenericStatus.Request.Status.DELAYED):
                                requests.remove(request)
                                LOG.debug('request tracking for id %s finished with status %s', id, openRequest.status.value)
                            request = (id, datetime.now(), maxDate)
                elif minDate < datetime.now():
                    requests.remove(request)
                    LOG.debug('request tracking for id %s removed, no requests seen until minimum time', id)
            if not requests:
                self.requests.pop(domain)
        if self.requests:
            self.__timer = Timer(5, self.update)
            self.__timer.daemon = True
            self.__timer.start()