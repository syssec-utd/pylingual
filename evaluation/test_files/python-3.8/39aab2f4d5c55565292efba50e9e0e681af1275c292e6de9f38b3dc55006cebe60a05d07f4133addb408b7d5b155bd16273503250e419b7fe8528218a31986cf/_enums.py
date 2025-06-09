from enum import Enum
__all__ = ['AlertRuleKind', 'AlertSeverity', 'AttackTactic', 'DataConnectorKind', 'DataTypeState', 'IncidentClassification', 'IncidentClassificationReason', 'IncidentSeverity', 'IncidentStatus', 'MicrosoftSecurityProductName', 'TriggerOperator']

class AlertRuleKind(str, Enum):
    """
    The alert rule kind
    """
    SCHEDULED = 'Scheduled'
    MICROSOFT_SECURITY_INCIDENT_CREATION = 'MicrosoftSecurityIncidentCreation'
    FUSION = 'Fusion'

class AlertSeverity(str, Enum):
    """
    The severity for alerts created by this alert rule.
    """
    HIGH = 'High'
    '\n    High severity\n    '
    MEDIUM = 'Medium'
    '\n    Medium severity\n    '
    LOW = 'Low'
    '\n    Low severity\n    '
    INFORMATIONAL = 'Informational'
    '\n    Informational severity\n    '

class AttackTactic(str, Enum):
    """
    The severity for alerts created by this alert rule.
    """
    INITIAL_ACCESS = 'InitialAccess'
    EXECUTION = 'Execution'
    PERSISTENCE = 'Persistence'
    PRIVILEGE_ESCALATION = 'PrivilegeEscalation'
    DEFENSE_EVASION = 'DefenseEvasion'
    CREDENTIAL_ACCESS = 'CredentialAccess'
    DISCOVERY = 'Discovery'
    LATERAL_MOVEMENT = 'LateralMovement'
    COLLECTION = 'Collection'
    EXFILTRATION = 'Exfiltration'
    COMMAND_AND_CONTROL = 'CommandAndControl'
    IMPACT = 'Impact'

class DataConnectorKind(str, Enum):
    """
    The data connector kind
    """
    AZURE_ACTIVE_DIRECTORY = 'AzureActiveDirectory'
    AZURE_SECURITY_CENTER = 'AzureSecurityCenter'
    MICROSOFT_CLOUD_APP_SECURITY = 'MicrosoftCloudAppSecurity'
    THREAT_INTELLIGENCE = 'ThreatIntelligence'
    OFFICE365 = 'Office365'
    AMAZON_WEB_SERVICES_CLOUD_TRAIL = 'AmazonWebServicesCloudTrail'
    AZURE_ADVANCED_THREAT_PROTECTION = 'AzureAdvancedThreatProtection'
    MICROSOFT_DEFENDER_ADVANCED_THREAT_PROTECTION = 'MicrosoftDefenderAdvancedThreatProtection'

class DataTypeState(str, Enum):
    """
    Describe whether this data type connection is enabled or not.
    """
    ENABLED = 'Enabled'
    DISABLED = 'Disabled'

class IncidentClassification(str, Enum):
    """
    The reason the incident was closed
    """
    UNDETERMINED = 'Undetermined'
    '\n    Incident classification was undetermined\n    '
    TRUE_POSITIVE = 'TruePositive'
    '\n    Incident was true positive\n    '
    BENIGN_POSITIVE = 'BenignPositive'
    '\n    Incident was benign positive\n    '
    FALSE_POSITIVE = 'FalsePositive'
    '\n    Incident was false positive\n    '

class IncidentClassificationReason(str, Enum):
    """
    The classification reason the incident was closed with
    """
    SUSPICIOUS_ACTIVITY = 'SuspiciousActivity'
    '\n    Classification reason was suspicious activity\n    '
    SUSPICIOUS_BUT_EXPECTED = 'SuspiciousButExpected'
    '\n    Classification reason was suspicious but expected\n    '
    INCORRECT_ALERT_LOGIC = 'IncorrectAlertLogic'
    '\n    Classification reason was incorrect alert logic\n    '
    INACCURATE_DATA = 'InaccurateData'
    '\n    Classification reason was inaccurate data\n    '

class IncidentSeverity(str, Enum):
    """
    The severity of the incident
    """
    HIGH = 'High'
    '\n    High severity\n    '
    MEDIUM = 'Medium'
    '\n    Medium severity\n    '
    LOW = 'Low'
    '\n    Low severity\n    '
    INFORMATIONAL = 'Informational'
    '\n    Informational severity\n    '

class IncidentStatus(str, Enum):
    """
    The status of the incident
    """
    NEW = 'New'
    "\n    An active incident which isn't being handled currently\n    "
    ACTIVE = 'Active'
    '\n    An active incident which is being handled\n    '
    CLOSED = 'Closed'
    '\n    A non-active incident\n    '

class MicrosoftSecurityProductName(str, Enum):
    """
    The alerts' productName on which the cases will be generated
    """
    MICROSOFT_CLOUD_APP_SECURITY = 'Microsoft Cloud App Security'
    AZURE_SECURITY_CENTER = 'Azure Security Center'
    AZURE_ADVANCED_THREAT_PROTECTION = 'Azure Advanced Threat Protection'
    AZURE_ACTIVE_DIRECTORY_IDENTITY_PROTECTION = 'Azure Active Directory Identity Protection'
    AZURE_SECURITY_CENTER_FOR_IO_T = 'Azure Security Center for IoT'

class TriggerOperator(str, Enum):
    """
    The operation against the threshold that triggers alert rule.
    """
    GREATER_THAN = 'GreaterThan'
    LESS_THAN = 'LessThan'
    EQUAL = 'Equal'
    NOT_EQUAL = 'NotEqual'