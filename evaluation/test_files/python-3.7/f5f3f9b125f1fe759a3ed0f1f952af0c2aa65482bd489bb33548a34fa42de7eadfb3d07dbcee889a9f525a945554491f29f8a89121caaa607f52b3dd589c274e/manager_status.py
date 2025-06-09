from phidata.utils.enums import ExtendedEnum

class K8sManagerStatus(ExtendedEnum):
    """Enum describing the current status of a K8sManager"""
    PRE_INIT = 'PRE_INIT'
    WORKER_READY = 'WORKER_READY'
    RESOURCES_ACTIVE = 'RESOURCES_ACTIVE'
    ERROR = 'ERROR'

    def can_create_resources(self) -> bool:
        return self in (K8sManagerStatus.WORKER_READY, K8sManagerStatus.RESOURCES_ACTIVE)

    def can_delete_resources(self) -> bool:
        return self in (K8sManagerStatus.WORKER_READY, K8sManagerStatus.RESOURCES_ACTIVE)

    def can_get_resources(self) -> bool:
        return self in (K8sManagerStatus.WORKER_READY, K8sManagerStatus.RESOURCES_ACTIVE)

    def can_read_resources(self) -> bool:
        return self in (K8sManagerStatus.WORKER_READY, K8sManagerStatus.RESOURCES_ACTIVE)