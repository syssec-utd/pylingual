import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
__all__ = ['AsyncOptionsResponse', 'AuditConfigResponse', 'AuditLogConfigResponse', 'BasicAuthResponse', 'BindingResponse', 'CollectionOverrideResponse', 'CompositeTypeLabelEntryResponse', 'ConfigFileResponse', 'CredentialResponse', 'DeploymentLabelEntryResponse', 'DeploymentUpdateLabelEntryResponse', 'DeploymentUpdateResponse', 'DiagnosticResponse', 'ExprResponse', 'ImportFileResponse', 'InputMappingResponse', 'OperationErrorErrorsItemResponse', 'OperationErrorResponse', 'OperationResponse', 'OperationWarningsItemDataItemResponse', 'OperationWarningsItemResponse', 'OptionsResponse', 'PollingOptionsResponse', 'ServiceAccountResponse', 'TargetConfigurationResponse', 'TemplateContentsResponse', 'TypeProviderLabelEntryResponse', 'ValidationOptionsResponse']

@pulumi.output_type
class AsyncOptionsResponse(dict):
    """
    Async options that determine when a resource should finish.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'methodMatch':
            suggest = 'method_match'
        elif key == 'pollingOptions':
            suggest = 'polling_options'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AsyncOptionsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AsyncOptionsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AsyncOptionsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, method_match: str, polling_options: 'outputs.PollingOptionsResponse'):
        """
        Async options that determine when a resource should finish.
        :param str method_match: Method regex where this policy will apply.
        :param 'PollingOptionsResponse' polling_options: Deployment manager will poll instances for this API resource setting a RUNNING state, and blocking until polling conditions tell whether the resource is completed or failed.
        """
        pulumi.set(__self__, 'method_match', method_match)
        pulumi.set(__self__, 'polling_options', polling_options)

    @property
    @pulumi.getter(name='methodMatch')
    def method_match(self) -> str:
        """
        Method regex where this policy will apply.
        """
        return pulumi.get(self, 'method_match')

    @property
    @pulumi.getter(name='pollingOptions')
    def polling_options(self) -> 'outputs.PollingOptionsResponse':
        """
        Deployment manager will poll instances for this API resource setting a RUNNING state, and blocking until polling conditions tell whether the resource is completed or failed.
        """
        return pulumi.get(self, 'polling_options')

@pulumi.output_type
class AuditConfigResponse(dict):
    """
    Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'auditLogConfigs':
            suggest = 'audit_log_configs'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuditConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuditConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AuditConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, audit_log_configs: Sequence['outputs.AuditLogConfigResponse'], service: str):
        """
        Specifies the audit configuration for a service. The configuration determines which permission types are logged, and what identities, if any, are exempted from logging. An AuditConfig must have one or more AuditLogConfigs. If there are AuditConfigs for both `allServices` and a specific service, the union of the two AuditConfigs is used for that service: the log_types specified in each AuditConfig are enabled, and the exempted_members in each AuditLogConfig are exempted. Example Policy with multiple AuditConfigs: { "audit_configs": [ { "service": "allServices", "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" }, { "log_type": "ADMIN_READ" } ] }, { "service": "sampleservice.googleapis.com", "audit_log_configs": [ { "log_type": "DATA_READ" }, { "log_type": "DATA_WRITE", "exempted_members": [ "user:aliya@example.com" ] } ] } ] } For sampleservice, this policy enables DATA_READ, DATA_WRITE and ADMIN_READ logging. It also exempts `jose@example.com` from DATA_READ logging, and `aliya@example.com` from DATA_WRITE logging.
        :param Sequence['AuditLogConfigResponse'] audit_log_configs: The configuration for logging of each type of permission.
        :param str service: Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        pulumi.set(__self__, 'audit_log_configs', audit_log_configs)
        pulumi.set(__self__, 'service', service)

    @property
    @pulumi.getter(name='auditLogConfigs')
    def audit_log_configs(self) -> Sequence['outputs.AuditLogConfigResponse']:
        """
        The configuration for logging of each type of permission.
        """
        return pulumi.get(self, 'audit_log_configs')

    @property
    @pulumi.getter
    def service(self) -> str:
        """
        Specifies a service that will be enabled for audit logging. For example, `storage.googleapis.com`, `cloudsql.googleapis.com`. `allServices` is a special value that covers all services.
        """
        return pulumi.get(self, 'service')

@pulumi.output_type
class AuditLogConfigResponse(dict):
    """
    Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'exemptedMembers':
            suggest = 'exempted_members'
        elif key == 'logType':
            suggest = 'log_type'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AuditLogConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AuditLogConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        AuditLogConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, exempted_members: Sequence[str], log_type: str):
        """
        Provides the configuration for logging a type of permissions. Example: { "audit_log_configs": [ { "log_type": "DATA_READ", "exempted_members": [ "user:jose@example.com" ] }, { "log_type": "DATA_WRITE" } ] } This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting jose@example.com from DATA_READ logging.
        :param Sequence[str] exempted_members: Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        :param str log_type: The log type that this config enables.
        """
        pulumi.set(__self__, 'exempted_members', exempted_members)
        pulumi.set(__self__, 'log_type', log_type)

    @property
    @pulumi.getter(name='exemptedMembers')
    def exempted_members(self) -> Sequence[str]:
        """
        Specifies the identities that do not cause logging for this type of permission. Follows the same format of Binding.members.
        """
        return pulumi.get(self, 'exempted_members')

    @property
    @pulumi.getter(name='logType')
    def log_type(self) -> str:
        """
        The log type that this config enables.
        """
        return pulumi.get(self, 'log_type')

@pulumi.output_type
class BasicAuthResponse(dict):
    """
    Basic Auth used as a credential.
    """

    def __init__(__self__, *, password: str, user: str):
        """
        Basic Auth used as a credential.
        """
        pulumi.set(__self__, 'password', password)
        pulumi.set(__self__, 'user', user)

    @property
    @pulumi.getter
    def password(self) -> str:
        return pulumi.get(self, 'password')

    @property
    @pulumi.getter
    def user(self) -> str:
        return pulumi.get(self, 'user')

@pulumi.output_type
class BindingResponse(dict):
    """
    Associates `members`, or principals, with a `role`.
    """

    def __init__(__self__, *, condition: 'outputs.ExprResponse', members: Sequence[str], role: str):
        """
        Associates `members`, or principals, with a `role`.
        :param 'ExprResponse' condition: The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        :param Sequence[str] members: Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        :param str role: Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        pulumi.set(__self__, 'condition', condition)
        pulumi.set(__self__, 'members', members)
        pulumi.set(__self__, 'role', role)

    @property
    @pulumi.getter
    def condition(self) -> 'outputs.ExprResponse':
        """
        The condition that is associated with this binding. If the condition evaluates to `true`, then this binding applies to the current request. If the condition evaluates to `false`, then this binding does not apply to the current request. However, a different role binding might grant the same role to one or more of the principals in this binding. To learn which resources support conditions in their IAM policies, see the [IAM documentation](https://cloud.google.com/iam/help/conditions/resource-policies).
        """
        return pulumi.get(self, 'condition')

    @property
    @pulumi.getter
    def members(self) -> Sequence[str]:
        """
        Specifies the principals requesting access for a Google Cloud resource. `members` can have the following values: * `allUsers`: A special identifier that represents anyone who is on the internet; with or without a Google account. * `allAuthenticatedUsers`: A special identifier that represents anyone who is authenticated with a Google account or a service account. Does not include identities that come from external identity providers (IdPs) through identity federation. * `user:{emailid}`: An email address that represents a specific Google account. For example, `alice@example.com` . * `serviceAccount:{emailid}`: An email address that represents a Google service account. For example, `my-other-app@appspot.gserviceaccount.com`. * `serviceAccount:{projectid}.svc.id.goog[{namespace}/{kubernetes-sa}]`: An identifier for a [Kubernetes service account](https://cloud.google.com/kubernetes-engine/docs/how-to/kubernetes-service-accounts). For example, `my-project.svc.id.goog[my-namespace/my-kubernetes-sa]`. * `group:{emailid}`: An email address that represents a Google group. For example, `admins@example.com`. * `deleted:user:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a user that has been recently deleted. For example, `alice@example.com?uid=123456789012345678901`. If the user is recovered, this value reverts to `user:{emailid}` and the recovered user retains the role in the binding. * `deleted:serviceAccount:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a service account that has been recently deleted. For example, `my-other-app@appspot.gserviceaccount.com?uid=123456789012345678901`. If the service account is undeleted, this value reverts to `serviceAccount:{emailid}` and the undeleted service account retains the role in the binding. * `deleted:group:{emailid}?uid={uniqueid}`: An email address (plus unique identifier) representing a Google group that has been recently deleted. For example, `admins@example.com?uid=123456789012345678901`. If the group is recovered, this value reverts to `group:{emailid}` and the recovered group retains the role in the binding. * `domain:{domain}`: The G Suite domain (primary) that represents all the users of that domain. For example, `google.com` or `example.com`. 
        """
        return pulumi.get(self, 'members')

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        Role that is assigned to the list of `members`, or principals. For example, `roles/viewer`, `roles/editor`, or `roles/owner`.
        """
        return pulumi.get(self, 'role')

@pulumi.output_type
class CollectionOverrideResponse(dict):
    """
    CollectionOverride allows resource handling overrides for specific resources within a BaseType
    """

    def __init__(__self__, *, collection: str, options: 'outputs.OptionsResponse'):
        """
        CollectionOverride allows resource handling overrides for specific resources within a BaseType
        :param str collection: The collection that identifies this resource within its service.
        :param 'OptionsResponse' options: The options to apply to this resource-level override
        """
        pulumi.set(__self__, 'collection', collection)
        pulumi.set(__self__, 'options', options)

    @property
    @pulumi.getter
    def collection(self) -> str:
        """
        The collection that identifies this resource within its service.
        """
        return pulumi.get(self, 'collection')

    @property
    @pulumi.getter
    def options(self) -> 'outputs.OptionsResponse':
        """
        The options to apply to this resource-level override
        """
        return pulumi.get(self, 'options')

@pulumi.output_type
class CompositeTypeLabelEntryResponse(dict):
    """
    Label object for CompositeTypes
    """

    def __init__(__self__, *, key: str, value: str):
        """
        Label object for CompositeTypes
        :param str key: Key of the label
        :param str value: Value of the label
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Key of the label
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the label
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class ConfigFileResponse(dict):

    def __init__(__self__, *, content: str):
        """
        :param str content: The contents of the file.
        """
        pulumi.set(__self__, 'content', content)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The contents of the file.
        """
        return pulumi.get(self, 'content')

@pulumi.output_type
class CredentialResponse(dict):
    """
    The credential used by Deployment Manager and TypeProvider. Only one of the options is permitted.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'basicAuth':
            suggest = 'basic_auth'
        elif key == 'serviceAccount':
            suggest = 'service_account'
        elif key == 'useProjectDefault':
            suggest = 'use_project_default'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CredentialResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CredentialResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CredentialResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, basic_auth: 'outputs.BasicAuthResponse', service_account: 'outputs.ServiceAccountResponse', use_project_default: bool):
        """
        The credential used by Deployment Manager and TypeProvider. Only one of the options is permitted.
        :param 'BasicAuthResponse' basic_auth: Basic Auth Credential, only used by TypeProvider.
        :param 'ServiceAccountResponse' service_account: Service Account Credential, only used by Deployment.
        :param bool use_project_default: Specify to use the project default credential, only supported by Deployment.
        """
        pulumi.set(__self__, 'basic_auth', basic_auth)
        pulumi.set(__self__, 'service_account', service_account)
        pulumi.set(__self__, 'use_project_default', use_project_default)

    @property
    @pulumi.getter(name='basicAuth')
    def basic_auth(self) -> 'outputs.BasicAuthResponse':
        """
        Basic Auth Credential, only used by TypeProvider.
        """
        return pulumi.get(self, 'basic_auth')

    @property
    @pulumi.getter(name='serviceAccount')
    def service_account(self) -> 'outputs.ServiceAccountResponse':
        """
        Service Account Credential, only used by Deployment.
        """
        return pulumi.get(self, 'service_account')

    @property
    @pulumi.getter(name='useProjectDefault')
    def use_project_default(self) -> bool:
        """
        Specify to use the project default credential, only supported by Deployment.
        """
        return pulumi.get(self, 'use_project_default')

@pulumi.output_type
class DeploymentLabelEntryResponse(dict):
    """
    Label object for Deployments
    """

    def __init__(__self__, *, key: str, value: str):
        """
        Label object for Deployments
        :param str key: Key of the label
        :param str value: Value of the label
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Key of the label
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the label
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class DeploymentUpdateLabelEntryResponse(dict):
    """
    Label object for DeploymentUpdate
    """

    def __init__(__self__, *, key: str, value: str):
        """
        Label object for DeploymentUpdate
        :param str key: Key of the label
        :param str value: Value of the label
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Key of the label
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the label
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class DeploymentUpdateResponse(dict):

    def __init__(__self__, *, description: str, labels: Sequence['outputs.DeploymentUpdateLabelEntryResponse'], manifest: str):
        """
        :param str description: An optional user-provided description of the deployment after the current update has been applied.
        :param Sequence['DeploymentUpdateLabelEntryResponse'] labels: Map of One Platform labels; provided by the client when the resource is created or updated. Specifically: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `[a-z]([-a-z0-9]*[a-z0-9])?` Label values must be between 0 and 63 characters long and must conform to the regular expression `([a-z]([-a-z0-9]*[a-z0-9])?)?`.
        :param str manifest: URL of the manifest representing the update configuration of this deployment.
        """
        pulumi.set(__self__, 'description', description)
        pulumi.set(__self__, 'labels', labels)
        pulumi.set(__self__, 'manifest', manifest)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        An optional user-provided description of the deployment after the current update has been applied.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def labels(self) -> Sequence['outputs.DeploymentUpdateLabelEntryResponse']:
        """
        Map of One Platform labels; provided by the client when the resource is created or updated. Specifically: Label keys must be between 1 and 63 characters long and must conform to the following regular expression: `[a-z]([-a-z0-9]*[a-z0-9])?` Label values must be between 0 and 63 characters long and must conform to the regular expression `([a-z]([-a-z0-9]*[a-z0-9])?)?`.
        """
        return pulumi.get(self, 'labels')

    @property
    @pulumi.getter
    def manifest(self) -> str:
        """
        URL of the manifest representing the update configuration of this deployment.
        """
        return pulumi.get(self, 'manifest')

@pulumi.output_type
class DiagnosticResponse(dict):

    def __init__(__self__, *, field: str, level: str):
        """
        :param str field: JsonPath expression on the resource that if non empty, indicates that this field needs to be extracted as a diagnostic.
        :param str level: Level to record this diagnostic.
        """
        pulumi.set(__self__, 'field', field)
        pulumi.set(__self__, 'level', level)

    @property
    @pulumi.getter
    def field(self) -> str:
        """
        JsonPath expression on the resource that if non empty, indicates that this field needs to be extracted as a diagnostic.
        """
        return pulumi.get(self, 'field')

    @property
    @pulumi.getter
    def level(self) -> str:
        """
        Level to record this diagnostic.
        """
        return pulumi.get(self, 'level')

@pulumi.output_type
class ExprResponse(dict):
    """
    Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
    """

    def __init__(__self__, *, description: str, expression: str, location: str, title: str):
        """
        Represents a textual expression in the Common Expression Language (CEL) syntax. CEL is a C-like expression language. The syntax and semantics of CEL are documented at https://github.com/google/cel-spec. Example (Comparison): title: "Summary size limit" description: "Determines if a summary is less than 100 chars" expression: "document.summary.size() < 100" Example (Equality): title: "Requestor is owner" description: "Determines if requestor is the document owner" expression: "document.owner == request.auth.claims.email" Example (Logic): title: "Public documents" description: "Determine whether the document should be publicly visible" expression: "document.type != 'private' && document.type != 'internal'" Example (Data Manipulation): title: "Notification string" description: "Create a notification string with a timestamp." expression: "'New message received at ' + string(document.create_time)" The exact variables and functions that may be referenced within an expression are determined by the service that evaluates it. See the service documentation for additional information.
        :param str description: Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        :param str expression: Textual representation of an expression in Common Expression Language syntax.
        :param str location: Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        :param str title: Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        pulumi.set(__self__, 'description', description)
        pulumi.set(__self__, 'expression', expression)
        pulumi.set(__self__, 'location', location)
        pulumi.set(__self__, 'title', title)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Optional. Description of the expression. This is a longer text which describes the expression, e.g. when hovered over it in a UI.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        Textual representation of an expression in Common Expression Language syntax.
        """
        return pulumi.get(self, 'expression')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Optional. String indicating the location of the expression for error reporting, e.g. a file name and a position in the file.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def title(self) -> str:
        """
        Optional. Title for the expression, i.e. a short string describing its purpose. This can be used e.g. in UIs which allow to enter the expression.
        """
        return pulumi.get(self, 'title')

@pulumi.output_type
class ImportFileResponse(dict):

    def __init__(__self__, *, content: str, name: str):
        """
        :param str content: The contents of the file.
        :param str name: The name of the file.
        """
        pulumi.set(__self__, 'content', content)
        pulumi.set(__self__, 'name', name)

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        The contents of the file.
        """
        return pulumi.get(self, 'content')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the file.
        """
        return pulumi.get(self, 'name')

@pulumi.output_type
class InputMappingResponse(dict):
    """
    InputMapping creates a 'virtual' property that will be injected into the properties before sending the request to the underlying API.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'fieldName':
            suggest = 'field_name'
        elif key == 'methodMatch':
            suggest = 'method_match'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in InputMappingResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        InputMappingResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        InputMappingResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, field_name: str, location: str, method_match: str, value: str):
        """
        InputMapping creates a 'virtual' property that will be injected into the properties before sending the request to the underlying API.
        :param str field_name: The name of the field that is going to be injected.
        :param str location: The location where this mapping applies.
        :param str method_match: Regex to evaluate on method to decide if input applies.
        :param str value: A jsonPath expression to select an element.
        """
        pulumi.set(__self__, 'field_name', field_name)
        pulumi.set(__self__, 'location', location)
        pulumi.set(__self__, 'method_match', method_match)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter(name='fieldName')
    def field_name(self) -> str:
        """
        The name of the field that is going to be injected.
        """
        return pulumi.get(self, 'field_name')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location where this mapping applies.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter(name='methodMatch')
    def method_match(self) -> str:
        """
        Regex to evaluate on method to decide if input applies.
        """
        return pulumi.get(self, 'method_match')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        A jsonPath expression to select an element.
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class OperationErrorErrorsItemResponse(dict):

    def __init__(__self__, *, code: str, location: str, message: str):
        """
        :param str code: The error type identifier for this error.
        :param str location: Indicates the field in the request that caused the error. This property is optional.
        :param str message: An optional, human-readable error message.
        """
        pulumi.set(__self__, 'code', code)
        pulumi.set(__self__, 'location', location)
        pulumi.set(__self__, 'message', message)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        The error type identifier for this error.
        """
        return pulumi.get(self, 'code')

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Indicates the field in the request that caused the error. This property is optional.
        """
        return pulumi.get(self, 'location')

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        An optional, human-readable error message.
        """
        return pulumi.get(self, 'message')

@pulumi.output_type
class OperationErrorResponse(dict):
    """
    [Output Only] If errors are generated during processing of the operation, this field will be populated.
    """

    def __init__(__self__, *, errors: Sequence['outputs.OperationErrorErrorsItemResponse']):
        """
        [Output Only] If errors are generated during processing of the operation, this field will be populated.
        :param Sequence['OperationErrorErrorsItemResponse'] errors: The array of errors encountered while processing this operation.
        """
        pulumi.set(__self__, 'errors', errors)

    @property
    @pulumi.getter
    def errors(self) -> Sequence['outputs.OperationErrorErrorsItemResponse']:
        """
        The array of errors encountered while processing this operation.
        """
        return pulumi.get(self, 'errors')

@pulumi.output_type
class OperationResponse(dict):
    """
    Represents an Operation resource. Google Compute Engine has three Operation resources: * [Global](/compute/docs/reference/rest/{$api_version}/globalOperations) * [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations) * [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations) You can use an operation resource to manage asynchronous API requests. For more information, read Handling API responses. Operations can be global, regional or zonal. - For global operations, use the `globalOperations` resource. - For regional operations, use the `regionOperations` resource. - For zonal operations, use the `zonalOperations` resource. For more information, read Global, Regional, and Zonal Resources.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'clientOperationId':
            suggest = 'client_operation_id'
        elif key == 'creationTimestamp':
            suggest = 'creation_timestamp'
        elif key == 'endTime':
            suggest = 'end_time'
        elif key == 'httpErrorMessage':
            suggest = 'http_error_message'
        elif key == 'httpErrorStatusCode':
            suggest = 'http_error_status_code'
        elif key == 'insertTime':
            suggest = 'insert_time'
        elif key == 'operationGroupId':
            suggest = 'operation_group_id'
        elif key == 'operationType':
            suggest = 'operation_type'
        elif key == 'selfLink':
            suggest = 'self_link'
        elif key == 'startTime':
            suggest = 'start_time'
        elif key == 'statusMessage':
            suggest = 'status_message'
        elif key == 'targetId':
            suggest = 'target_id'
        elif key == 'targetLink':
            suggest = 'target_link'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OperationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OperationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        OperationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, client_operation_id: str, creation_timestamp: str, description: str, end_time: str, error: 'outputs.OperationErrorResponse', http_error_message: str, http_error_status_code: int, insert_time: str, kind: str, name: str, operation_group_id: str, operation_type: str, progress: int, region: str, self_link: str, start_time: str, status: str, status_message: str, target_id: str, target_link: str, user: str, warnings: Sequence['outputs.OperationWarningsItemResponse'], zone: str):
        """
        Represents an Operation resource. Google Compute Engine has three Operation resources: * [Global](/compute/docs/reference/rest/{$api_version}/globalOperations) * [Regional](/compute/docs/reference/rest/{$api_version}/regionOperations) * [Zonal](/compute/docs/reference/rest/{$api_version}/zoneOperations) You can use an operation resource to manage asynchronous API requests. For more information, read Handling API responses. Operations can be global, regional or zonal. - For global operations, use the `globalOperations` resource. - For regional operations, use the `regionOperations` resource. - For zonal operations, use the `zonalOperations` resource. For more information, read Global, Regional, and Zonal Resources.
        :param str client_operation_id: The value of `requestId` if you provided it in the request. Not present otherwise.
        :param str creation_timestamp: [Deprecated] This field is deprecated.
        :param str description: A textual description of the operation, which is set when the operation is created.
        :param str end_time: The time that this operation was completed. This value is in RFC3339 text format.
        :param 'OperationErrorResponse' error: If errors are generated during processing of the operation, this field will be populated.
        :param str http_error_message: If the operation fails, this field contains the HTTP error message that was returned, such as `NOT FOUND`.
        :param int http_error_status_code: If the operation fails, this field contains the HTTP error status code that was returned. For example, a `404` means the resource was not found.
        :param str insert_time: The time that this operation was requested. This value is in RFC3339 text format.
        :param str kind: Type of the resource. Always `compute#operation` for Operation resources.
        :param str name: Name of the operation.
        :param str operation_group_id: An ID that represents a group of operations, such as when a group of operations results from a `bulkInsert` API request.
        :param str operation_type: The type of operation, such as `insert`, `update`, or `delete`, and so on.
        :param int progress: An optional progress indicator that ranges from 0 to 100. There is no requirement that this be linear or support any granularity of operations. This should not be used to guess when the operation will be complete. This number should monotonically increase as the operation progresses.
        :param str region: The URL of the region where the operation resides. Only applicable when performing regional operations.
        :param str self_link: Server-defined URL for the resource.
        :param str start_time: The time that this operation was started by the server. This value is in RFC3339 text format.
        :param str status: The status of the operation, which can be one of the following: `PENDING`, `RUNNING`, or `DONE`.
        :param str status_message: An optional textual description of the current status of the operation.
        :param str target_id: The unique target ID, which identifies a specific incarnation of the target resource.
        :param str target_link: The URL of the resource that the operation modifies. For operations related to creating a snapshot, this points to the persistent disk that the snapshot was created from.
        :param str user: User who requested the operation, for example: `user@example.com`.
        :param Sequence['OperationWarningsItemResponse'] warnings: If warning messages are generated during processing of the operation, this field will be populated.
        :param str zone: The URL of the zone where the operation resides. Only applicable when performing per-zone operations.
        """
        pulumi.set(__self__, 'client_operation_id', client_operation_id)
        pulumi.set(__self__, 'creation_timestamp', creation_timestamp)
        pulumi.set(__self__, 'description', description)
        pulumi.set(__self__, 'end_time', end_time)
        pulumi.set(__self__, 'error', error)
        pulumi.set(__self__, 'http_error_message', http_error_message)
        pulumi.set(__self__, 'http_error_status_code', http_error_status_code)
        pulumi.set(__self__, 'insert_time', insert_time)
        pulumi.set(__self__, 'kind', kind)
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'operation_group_id', operation_group_id)
        pulumi.set(__self__, 'operation_type', operation_type)
        pulumi.set(__self__, 'progress', progress)
        pulumi.set(__self__, 'region', region)
        pulumi.set(__self__, 'self_link', self_link)
        pulumi.set(__self__, 'start_time', start_time)
        pulumi.set(__self__, 'status', status)
        pulumi.set(__self__, 'status_message', status_message)
        pulumi.set(__self__, 'target_id', target_id)
        pulumi.set(__self__, 'target_link', target_link)
        pulumi.set(__self__, 'user', user)
        pulumi.set(__self__, 'warnings', warnings)
        pulumi.set(__self__, 'zone', zone)

    @property
    @pulumi.getter(name='clientOperationId')
    def client_operation_id(self) -> str:
        """
        The value of `requestId` if you provided it in the request. Not present otherwise.
        """
        return pulumi.get(self, 'client_operation_id')

    @property
    @pulumi.getter(name='creationTimestamp')
    def creation_timestamp(self) -> str:
        """
        [Deprecated] This field is deprecated.
        """
        return pulumi.get(self, 'creation_timestamp')

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A textual description of the operation, which is set when the operation is created.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='endTime')
    def end_time(self) -> str:
        """
        The time that this operation was completed. This value is in RFC3339 text format.
        """
        return pulumi.get(self, 'end_time')

    @property
    @pulumi.getter
    def error(self) -> 'outputs.OperationErrorResponse':
        """
        If errors are generated during processing of the operation, this field will be populated.
        """
        return pulumi.get(self, 'error')

    @property
    @pulumi.getter(name='httpErrorMessage')
    def http_error_message(self) -> str:
        """
        If the operation fails, this field contains the HTTP error message that was returned, such as `NOT FOUND`.
        """
        return pulumi.get(self, 'http_error_message')

    @property
    @pulumi.getter(name='httpErrorStatusCode')
    def http_error_status_code(self) -> int:
        """
        If the operation fails, this field contains the HTTP error status code that was returned. For example, a `404` means the resource was not found.
        """
        return pulumi.get(self, 'http_error_status_code')

    @property
    @pulumi.getter(name='insertTime')
    def insert_time(self) -> str:
        """
        The time that this operation was requested. This value is in RFC3339 text format.
        """
        return pulumi.get(self, 'insert_time')

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Type of the resource. Always `compute#operation` for Operation resources.
        """
        return pulumi.get(self, 'kind')

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the operation.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='operationGroupId')
    def operation_group_id(self) -> str:
        """
        An ID that represents a group of operations, such as when a group of operations results from a `bulkInsert` API request.
        """
        return pulumi.get(self, 'operation_group_id')

    @property
    @pulumi.getter(name='operationType')
    def operation_type(self) -> str:
        """
        The type of operation, such as `insert`, `update`, or `delete`, and so on.
        """
        return pulumi.get(self, 'operation_type')

    @property
    @pulumi.getter
    def progress(self) -> int:
        """
        An optional progress indicator that ranges from 0 to 100. There is no requirement that this be linear or support any granularity of operations. This should not be used to guess when the operation will be complete. This number should monotonically increase as the operation progresses.
        """
        return pulumi.get(self, 'progress')

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        The URL of the region where the operation resides. Only applicable when performing regional operations.
        """
        return pulumi.get(self, 'region')

    @property
    @pulumi.getter(name='selfLink')
    def self_link(self) -> str:
        """
        Server-defined URL for the resource.
        """
        return pulumi.get(self, 'self_link')

    @property
    @pulumi.getter(name='startTime')
    def start_time(self) -> str:
        """
        The time that this operation was started by the server. This value is in RFC3339 text format.
        """
        return pulumi.get(self, 'start_time')

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the operation, which can be one of the following: `PENDING`, `RUNNING`, or `DONE`.
        """
        return pulumi.get(self, 'status')

    @property
    @pulumi.getter(name='statusMessage')
    def status_message(self) -> str:
        """
        An optional textual description of the current status of the operation.
        """
        return pulumi.get(self, 'status_message')

    @property
    @pulumi.getter(name='targetId')
    def target_id(self) -> str:
        """
        The unique target ID, which identifies a specific incarnation of the target resource.
        """
        return pulumi.get(self, 'target_id')

    @property
    @pulumi.getter(name='targetLink')
    def target_link(self) -> str:
        """
        The URL of the resource that the operation modifies. For operations related to creating a snapshot, this points to the persistent disk that the snapshot was created from.
        """
        return pulumi.get(self, 'target_link')

    @property
    @pulumi.getter
    def user(self) -> str:
        """
        User who requested the operation, for example: `user@example.com`.
        """
        return pulumi.get(self, 'user')

    @property
    @pulumi.getter
    def warnings(self) -> Sequence['outputs.OperationWarningsItemResponse']:
        """
        If warning messages are generated during processing of the operation, this field will be populated.
        """
        return pulumi.get(self, 'warnings')

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        The URL of the zone where the operation resides. Only applicable when performing per-zone operations.
        """
        return pulumi.get(self, 'zone')

@pulumi.output_type
class OperationWarningsItemDataItemResponse(dict):

    def __init__(__self__, *, key: str, value: str):
        """
        :param str key: A key that provides more detail on the warning being returned. For example, for warnings where there are no results in a list request for a particular zone, this key might be scope and the key value might be the zone name. Other examples might be a key indicating a deprecated resource and a suggested replacement, or a warning about invalid network settings (for example, if an instance attempts to perform IP forwarding but is not enabled for IP forwarding).
        :param str value: A warning data value corresponding to the key.
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        A key that provides more detail on the warning being returned. For example, for warnings where there are no results in a list request for a particular zone, this key might be scope and the key value might be the zone name. Other examples might be a key indicating a deprecated resource and a suggested replacement, or a warning about invalid network settings (for example, if an instance attempts to perform IP forwarding but is not enabled for IP forwarding).
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        A warning data value corresponding to the key.
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class OperationWarningsItemResponse(dict):

    def __init__(__self__, *, code: str, data: Sequence['outputs.OperationWarningsItemDataItemResponse'], message: str):
        """
        :param str code: A warning code, if applicable. For example, Compute Engine returns NO_RESULTS_ON_PAGE if there are no results in the response.
        :param Sequence['OperationWarningsItemDataItemResponse'] data: Metadata about this warning in key: value format. For example: "data": [ { "key": "scope", "value": "zones/us-east1-d" } 
        :param str message: A human-readable description of the warning code.
        """
        pulumi.set(__self__, 'code', code)
        pulumi.set(__self__, 'data', data)
        pulumi.set(__self__, 'message', message)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        A warning code, if applicable. For example, Compute Engine returns NO_RESULTS_ON_PAGE if there are no results in the response.
        """
        return pulumi.get(self, 'code')

    @property
    @pulumi.getter
    def data(self) -> Sequence['outputs.OperationWarningsItemDataItemResponse']:
        """
        Metadata about this warning in key: value format. For example: "data": [ { "key": "scope", "value": "zones/us-east1-d" } 
        """
        return pulumi.get(self, 'data')

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        A human-readable description of the warning code.
        """
        return pulumi.get(self, 'message')

@pulumi.output_type
class OptionsResponse(dict):
    """
    Options allows customized resource handling by Deployment Manager.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'asyncOptions':
            suggest = 'async_options'
        elif key == 'inputMappings':
            suggest = 'input_mappings'
        elif key == 'validationOptions':
            suggest = 'validation_options'
        elif key == 'virtualProperties':
            suggest = 'virtual_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OptionsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OptionsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        OptionsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, async_options: Sequence['outputs.AsyncOptionsResponse'], input_mappings: Sequence['outputs.InputMappingResponse'], validation_options: 'outputs.ValidationOptionsResponse', virtual_properties: str):
        """
        Options allows customized resource handling by Deployment Manager.
        :param Sequence['AsyncOptionsResponse'] async_options: Options regarding how to thread async requests.
        :param Sequence['InputMappingResponse'] input_mappings: The mappings that apply for requests.
        :param 'ValidationOptionsResponse' validation_options: Options for how to validate and process properties on a resource.
        :param str virtual_properties: Additional properties block described as a jsonSchema, these properties will never be part of the json payload, but they can be consumed by InputMappings, this must be a valid json schema draft-04. The properties specified here will be decouple in a different section. This schema will be merged to the schema validation, and properties here will be extracted From the payload and consumed explicitly by InputMappings. ex: field1: type: string field2: type: number
        """
        pulumi.set(__self__, 'async_options', async_options)
        pulumi.set(__self__, 'input_mappings', input_mappings)
        pulumi.set(__self__, 'validation_options', validation_options)
        pulumi.set(__self__, 'virtual_properties', virtual_properties)

    @property
    @pulumi.getter(name='asyncOptions')
    def async_options(self) -> Sequence['outputs.AsyncOptionsResponse']:
        """
        Options regarding how to thread async requests.
        """
        return pulumi.get(self, 'async_options')

    @property
    @pulumi.getter(name='inputMappings')
    def input_mappings(self) -> Sequence['outputs.InputMappingResponse']:
        """
        The mappings that apply for requests.
        """
        return pulumi.get(self, 'input_mappings')

    @property
    @pulumi.getter(name='validationOptions')
    def validation_options(self) -> 'outputs.ValidationOptionsResponse':
        """
        Options for how to validate and process properties on a resource.
        """
        return pulumi.get(self, 'validation_options')

    @property
    @pulumi.getter(name='virtualProperties')
    def virtual_properties(self) -> str:
        """
        Additional properties block described as a jsonSchema, these properties will never be part of the json payload, but they can be consumed by InputMappings, this must be a valid json schema draft-04. The properties specified here will be decouple in a different section. This schema will be merged to the schema validation, and properties here will be extracted From the payload and consumed explicitly by InputMappings. ex: field1: type: string field2: type: number
        """
        return pulumi.get(self, 'virtual_properties')

@pulumi.output_type
class PollingOptionsResponse(dict):

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'failCondition':
            suggest = 'fail_condition'
        elif key == 'finishCondition':
            suggest = 'finish_condition'
        elif key == 'pollingLink':
            suggest = 'polling_link'
        elif key == 'targetLink':
            suggest = 'target_link'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PollingOptionsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PollingOptionsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        PollingOptionsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, diagnostics: Sequence['outputs.DiagnosticResponse'], fail_condition: str, finish_condition: str, polling_link: str, target_link: str):
        """
        :param Sequence['DiagnosticResponse'] diagnostics: An array of diagnostics to be collected by Deployment Manager, these diagnostics will be displayed to the user.
        :param str fail_condition: JsonPath expression that determines if the request failed.
        :param str finish_condition: JsonPath expression that determines if the request is completed.
        :param str polling_link: JsonPath expression that evaluates to string, it indicates where to poll.
        :param str target_link: JsonPath expression, after polling is completed, indicates where to fetch the resource.
        """
        pulumi.set(__self__, 'diagnostics', diagnostics)
        pulumi.set(__self__, 'fail_condition', fail_condition)
        pulumi.set(__self__, 'finish_condition', finish_condition)
        pulumi.set(__self__, 'polling_link', polling_link)
        pulumi.set(__self__, 'target_link', target_link)

    @property
    @pulumi.getter
    def diagnostics(self) -> Sequence['outputs.DiagnosticResponse']:
        """
        An array of diagnostics to be collected by Deployment Manager, these diagnostics will be displayed to the user.
        """
        return pulumi.get(self, 'diagnostics')

    @property
    @pulumi.getter(name='failCondition')
    def fail_condition(self) -> str:
        """
        JsonPath expression that determines if the request failed.
        """
        return pulumi.get(self, 'fail_condition')

    @property
    @pulumi.getter(name='finishCondition')
    def finish_condition(self) -> str:
        """
        JsonPath expression that determines if the request is completed.
        """
        return pulumi.get(self, 'finish_condition')

    @property
    @pulumi.getter(name='pollingLink')
    def polling_link(self) -> str:
        """
        JsonPath expression that evaluates to string, it indicates where to poll.
        """
        return pulumi.get(self, 'polling_link')

    @property
    @pulumi.getter(name='targetLink')
    def target_link(self) -> str:
        """
        JsonPath expression, after polling is completed, indicates where to fetch the resource.
        """
        return pulumi.get(self, 'target_link')

@pulumi.output_type
class ServiceAccountResponse(dict):
    """
    Service Account used as a credential.
    """

    def __init__(__self__, *, email: str):
        """
        Service Account used as a credential.
        :param str email: The IAM service account email address like test@myproject.iam.gserviceaccount.com
        """
        pulumi.set(__self__, 'email', email)

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        The IAM service account email address like test@myproject.iam.gserviceaccount.com
        """
        return pulumi.get(self, 'email')

@pulumi.output_type
class TargetConfigurationResponse(dict):

    def __init__(__self__, *, config: 'outputs.ConfigFileResponse', imports: Sequence['outputs.ImportFileResponse']):
        """
        :param 'ConfigFileResponse' config: The configuration to use for this deployment.
        :param Sequence['ImportFileResponse'] imports: Specifies any files to import for this configuration. This can be used to import templates or other files. For example, you might import a text file in order to use the file in a template.
        """
        pulumi.set(__self__, 'config', config)
        pulumi.set(__self__, 'imports', imports)

    @property
    @pulumi.getter
    def config(self) -> 'outputs.ConfigFileResponse':
        """
        The configuration to use for this deployment.
        """
        return pulumi.get(self, 'config')

    @property
    @pulumi.getter
    def imports(self) -> Sequence['outputs.ImportFileResponse']:
        """
        Specifies any files to import for this configuration. This can be used to import templates or other files. For example, you might import a text file in order to use the file in a template.
        """
        return pulumi.get(self, 'imports')

@pulumi.output_type
class TemplateContentsResponse(dict):
    """
    Files that make up the template contents of a template type.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'mainTemplate':
            suggest = 'main_template'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TemplateContentsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TemplateContentsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        TemplateContentsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, imports: Sequence['outputs.ImportFileResponse'], interpreter: str, main_template: str, schema: str, template: str):
        """
        Files that make up the template contents of a template type.
        :param Sequence['ImportFileResponse'] imports: Import files referenced by the main template.
        :param str interpreter: Which interpreter (python or jinja) should be used during expansion.
        :param str main_template: The filename of the mainTemplate
        :param str schema: The contents of the template schema.
        :param str template: The contents of the main template file.
        """
        pulumi.set(__self__, 'imports', imports)
        pulumi.set(__self__, 'interpreter', interpreter)
        pulumi.set(__self__, 'main_template', main_template)
        pulumi.set(__self__, 'schema', schema)
        pulumi.set(__self__, 'template', template)

    @property
    @pulumi.getter
    def imports(self) -> Sequence['outputs.ImportFileResponse']:
        """
        Import files referenced by the main template.
        """
        return pulumi.get(self, 'imports')

    @property
    @pulumi.getter
    def interpreter(self) -> str:
        """
        Which interpreter (python or jinja) should be used during expansion.
        """
        return pulumi.get(self, 'interpreter')

    @property
    @pulumi.getter(name='mainTemplate')
    def main_template(self) -> str:
        """
        The filename of the mainTemplate
        """
        return pulumi.get(self, 'main_template')

    @property
    @pulumi.getter
    def schema(self) -> str:
        """
        The contents of the template schema.
        """
        return pulumi.get(self, 'schema')

    @property
    @pulumi.getter
    def template(self) -> str:
        """
        The contents of the main template file.
        """
        return pulumi.get(self, 'template')

@pulumi.output_type
class TypeProviderLabelEntryResponse(dict):
    """
    Label object for TypeProviders
    """

    def __init__(__self__, *, key: str, value: str):
        """
        Label object for TypeProviders
        :param str key: Key of the label
        :param str value: Value of the label
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'value', value)

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        Key of the label
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the label
        """
        return pulumi.get(self, 'value')

@pulumi.output_type
class ValidationOptionsResponse(dict):
    """
    Options for how to validate and process properties on a resource.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'schemaValidation':
            suggest = 'schema_validation'
        elif key == 'undeclaredProperties':
            suggest = 'undeclared_properties'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ValidationOptionsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ValidationOptionsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ValidationOptionsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, schema_validation: str, undeclared_properties: str):
        """
        Options for how to validate and process properties on a resource.
        :param str schema_validation: Customize how deployment manager will validate the resource against schema errors.
        :param str undeclared_properties: Specify what to do with extra properties when executing a request.
        """
        pulumi.set(__self__, 'schema_validation', schema_validation)
        pulumi.set(__self__, 'undeclared_properties', undeclared_properties)

    @property
    @pulumi.getter(name='schemaValidation')
    def schema_validation(self) -> str:
        """
        Customize how deployment manager will validate the resource against schema errors.
        """
        return pulumi.get(self, 'schema_validation')

    @property
    @pulumi.getter(name='undeclaredProperties')
    def undeclared_properties(self) -> str:
        """
        Specify what to do with extra properties when executing a request.
        """
        return pulumi.get(self, 'undeclared_properties')