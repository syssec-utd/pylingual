import logging
from typing import List, Optional
from localstack.constants import APPLICATION_OCTET_STREAM
from localstack.http import Response
from localstack_ext.bootstrap.pods.servicestate.service_state import ServiceState
from localstack_ext.bootstrap.pods.utils.adapters import ServiceStateMarshaller
LOG = logging.getLogger(__name__)

def handle_get_state_request_in_memory(services=None):
    from localstack.services.plugins import SERVICE_PLUGINS as C
    F = C.list_loaded_services()
    A = ServiceState()
    for B in services or F:
        D = C.get_service_container(B)
        if not D:
            LOG.debug("Can't get service container for service %s while calling handle_get_state_request_in_memory", B)
        E = D.service.backend_state_lifecycle
        if E:
            try:
                G = E.retrieve_state()
                A.put_service_state(G)
            except Exception as H:
                LOG.debug('Unable to retrieve the state for service %s: %s - skipping', B, H)
    if A.is_empty():
        LOG.debug('Extracted state is empty')
    I = ServiceStateMarshaller.marshall(state=A)
    J = Response(I, mimetype=APPLICATION_OCTET_STREAM)
    return J