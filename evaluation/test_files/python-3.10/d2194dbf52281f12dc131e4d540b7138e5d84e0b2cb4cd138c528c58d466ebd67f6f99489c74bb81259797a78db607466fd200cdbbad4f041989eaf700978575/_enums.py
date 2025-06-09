from enum import Enum
__all__ = ['DataSourceKind', 'EntityStatus', 'MachineGroupType', 'SkuNameEnum']

class DataSourceKind(str, Enum):
    """
    The kind of the DataSource.
    """
    AZURE_ACTIVITY_LOG = 'AzureActivityLog'
    CHANGE_TRACKING_PATH = 'ChangeTrackingPath'
    CHANGE_TRACKING_DEFAULT_PATH = 'ChangeTrackingDefaultPath'
    CHANGE_TRACKING_DEFAULT_REGISTRY = 'ChangeTrackingDefaultRegistry'
    CHANGE_TRACKING_CUSTOM_REGISTRY = 'ChangeTrackingCustomRegistry'
    CUSTOM_LOG = 'CustomLog'
    CUSTOM_LOG_COLLECTION = 'CustomLogCollection'
    GENERIC_DATA_SOURCE = 'GenericDataSource'
    IIS_LOGS = 'IISLogs'
    LINUX_PERFORMANCE_OBJECT = 'LinuxPerformanceObject'
    LINUX_PERFORMANCE_COLLECTION = 'LinuxPerformanceCollection'
    LINUX_SYSLOG = 'LinuxSyslog'
    LINUX_SYSLOG_COLLECTION = 'LinuxSyslogCollection'
    WINDOWS_EVENT = 'WindowsEvent'
    WINDOWS_PERFORMANCE_COUNTER = 'WindowsPerformanceCounter'

class EntityStatus(str, Enum):
    """
    The provisioning state of the workspace.
    """
    CREATING = 'Creating'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    CANCELED = 'Canceled'
    DELETING = 'Deleting'
    PROVISIONING_ACCOUNT = 'ProvisioningAccount'

class MachineGroupType(str, Enum):
    """
    Type of the machine group
    """
    UNKNOWN = 'unknown'
    AZURE_CS = 'azure-cs'
    AZURE_SF = 'azure-sf'
    AZURE_VMSS = 'azure-vmss'
    USER_STATIC = 'user-static'

class SkuNameEnum(str, Enum):
    """
    The name of the SKU.
    """
    FREE = 'Free'
    STANDARD = 'Standard'
    PREMIUM = 'Premium'
    PER_NODE = 'PerNode'
    PER_GB2018 = 'PerGB2018'
    STANDALONE = 'Standalone'
    CAPACITY_RESERVATION = 'CapacityReservation'