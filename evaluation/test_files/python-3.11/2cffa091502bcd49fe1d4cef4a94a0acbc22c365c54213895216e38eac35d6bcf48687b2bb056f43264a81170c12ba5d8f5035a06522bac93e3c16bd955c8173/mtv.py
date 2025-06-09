from ocp_resources.utils import TimeoutExpiredError, TimeoutSampler

def _get_status_condition_log_message(**status_condition):
    log_msg = 'Waiting For: \n'
    for status_condition_name, status_condition in status_condition.items():
        log_msg += f'{status_condition_name}->{status_condition} \n' if status_condition else ''
    return log_msg

class MTV:
    """
    Abstract Class for all Migration ToolKit For Virtualization (MTV) Resources:
        Provider
        Plan
        Migration
        StorageMap
        NetworkMap
        Host
        ForkliftController
    """

    def __init__(self):
        self.api = None
        self.name = None
        self.namespace = None
        self.kind = None
        self.Condition = None
        self.Status = None
        self.condition_message_ready = None
        self.condition_message_succeeded = None
        self.mapping = None
        self.source_provider_name = None
        self.source_provider_namespace = None
        self.destination_provider_name = None
        self.destination_provider_namespace = None
        if self.__class__.__name__ == 'MTV':
            raise TypeError('MTV is not a Resource. Please Use one of its successors.')

    class ConditionMessage:
        PROVIDER_READY = 'The provider is ready.'
        NETWORK_MAP_READY = 'The network map is ready.'
        STORAGE_MAP_READY = 'The storage map is ready.'
        PLAN_READY = 'The migration plan is ready.'
        PLAN_SUCCEEDED = 'The plan execution has SUCCEEDED.'
        PLAN_FAILED = 'The plan execution has FAILED.'
        MIGRATION_READY = 'The migration is ready.'
        MIGRATION_RUNNING = 'The migration is RUNNING'
        MIGRATION_SUCCEEDED = 'The migration has SUCCEEDED.'
        HOST_READY = 'The host is ready.'

    class ConditionCategory:
        CRITICAL = 'Critical'

    class ConditionType:
        SUCCEEDED = 'Succeeded'
        FAILED = 'Failed'
        TARGET_NAME_NOT_VALID = 'TargetNameNotValid'
        VM_ALREADY_EXISTS = 'VMAlreadyExists'

    class ProviderType:
        VSPHERE = 'vsphere'
        OPENSHIFT = 'openshift'
        RHV = 'ovirt'

    def wait_for_resource_status(self, condition_status, condition_type, condition_message=None, condition_reason=None, condition_category=None, wait_timeout=600):
        """
        Wait for MTV Resource Status Conditions.
        """
        self.logger.info(_get_status_condition_log_message(condition_status=condition_status, condition_type=condition_type, condition_message=condition_message, condition_reason=condition_reason, condition_category=condition_category))
        samples = TimeoutSampler(wait_timeout=wait_timeout, sleep=1, func=self.api.get, field_selector=f'metadata.name=={self.name}', namespace=self.namespace)
        last_condition = None
        try:
            for sample in samples:
                current_conditions = sample.items[0].status.get('conditions') if sample.items and sample.items[0].status else []
                for condition in current_conditions:
                    last_condition = condition
                    valid_status_type = condition_status == condition.status and condition_type == condition.type
                    valid_message = condition_message == condition.message or condition_message is None
                    valid_reason = condition_reason == condition.reason or condition_reason is None
                    valid_category = condition_category == condition.category or condition_category is None
                    if all([valid_status_type, valid_message, valid_reason, valid_category]):
                        return
        except TimeoutExpiredError:
            self.logger.error(msg=f'Last Status Condition of {self.kind} {self.name} was: {last_condition}')
            raise

    def wait_for_condition_ready(self, wait_timeout=360):
        self.wait_for_resource_status(condition_message=self.condition_message_ready, condition_status=self.Condition.Status.TRUE, condition_type=self.Condition.READY, wait_timeout=wait_timeout)

    def wait_for_condition_succeeded(self, wait_timeout=600):
        self.wait_for_resource_status(condition_type=self.Status.SUCCEEDED, condition_message=self.condition_message_succeeded, condition_status=self.Condition.Status.TRUE, wait_timeout=wait_timeout)

    @property
    def map_to_dict(self):
        return {'spec': {'map': self.mapping, 'provider': {'source': {'name': self.source_provider_name, 'namespace': self.source_provider_namespace}, 'destination': {'name': self.destination_provider_name, 'namespace': self.destination_provider_namespace}}}}