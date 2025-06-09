from __future__ import annotations
from datetime import datetime
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
if TYPE_CHECKING:
    from . import analyzed_message_evidence, cloud_application_evidence, device_evidence, evidence_remediation_status, evidence_role, evidence_verdict, file_evidence, ip_evidence, mailbox_evidence, mail_cluster_evidence, oauth_application_evidence, process_evidence, registry_key_evidence, registry_value_evidence, security_group_evidence, url_evidence, user_evidence

class AlertEvidence(AdditionalDataHolder, Parsable):

    def __init__(self) -> None:
        """
        Instantiates a new alertEvidence and sets the default values.
        """
        self._additional_data: Dict[str, Any] = {}
        self._created_date_time: Optional[datetime] = None
        self._odata_type: Optional[str] = None
        self._remediation_status: Optional[evidence_remediation_status.EvidenceRemediationStatus] = None
        self._remediation_status_details: Optional[str] = None
        self._roles: Optional[List[evidence_role.EvidenceRole]] = None
        self._tags: Optional[List[str]] = None
        self._verdict: Optional[evidence_verdict.EvidenceVerdict] = None

    @property
    def additional_data(self) -> Dict[str, Any]:
        """
        Gets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Returns: Dict[str, Any]
        """
        return self._additional_data

    @additional_data.setter
    def additional_data(self, value: Dict[str, Any]) -> None:
        """
        Sets the additionalData property value. Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
        Args:
            value: Value to set for the AdditionalData property.
        """
        self._additional_data = value

    @property
    def created_date_time(self) -> Optional[datetime]:
        """
        Gets the createdDateTime property value. The time the evidence was created and added to the alert.
        Returns: Optional[datetime]
        """
        return self._created_date_time

    @created_date_time.setter
    def created_date_time(self, value: Optional[datetime]=None) -> None:
        """
        Sets the createdDateTime property value. The time the evidence was created and added to the alert.
        Args:
            value: Value to set for the created_date_time property.
        """
        self._created_date_time = value

    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode]=None) -> AlertEvidence:
        """
        Creates a new instance of the appropriate class based on discriminator value
        Args:
            parseNode: The parse node to use to read the discriminator value and create the object
        Returns: AlertEvidence
        """
        if parse_node is None:
            raise Exception('parse_node cannot be undefined')
        mapping_value_node = parse_node.get_child_node('@odata.type')
        if mapping_value_node:
            mapping_value = mapping_value_node.get_str_value()
            if mapping_value == '#microsoft.graph.security.analyzedMessageEvidence':
                from . import analyzed_message_evidence
                return analyzed_message_evidence.AnalyzedMessageEvidence()
            if mapping_value == '#microsoft.graph.security.cloudApplicationEvidence':
                from . import cloud_application_evidence
                return cloud_application_evidence.CloudApplicationEvidence()
            if mapping_value == '#microsoft.graph.security.deviceEvidence':
                from . import device_evidence
                return device_evidence.DeviceEvidence()
            if mapping_value == '#microsoft.graph.security.fileEvidence':
                from . import file_evidence
                return file_evidence.FileEvidence()
            if mapping_value == '#microsoft.graph.security.ipEvidence':
                from . import ip_evidence
                return ip_evidence.IpEvidence()
            if mapping_value == '#microsoft.graph.security.mailboxEvidence':
                from . import mailbox_evidence
                return mailbox_evidence.MailboxEvidence()
            if mapping_value == '#microsoft.graph.security.mailClusterEvidence':
                from . import mail_cluster_evidence
                return mail_cluster_evidence.MailClusterEvidence()
            if mapping_value == '#microsoft.graph.security.oauthApplicationEvidence':
                from . import oauth_application_evidence
                return oauth_application_evidence.OauthApplicationEvidence()
            if mapping_value == '#microsoft.graph.security.processEvidence':
                from . import process_evidence
                return process_evidence.ProcessEvidence()
            if mapping_value == '#microsoft.graph.security.registryKeyEvidence':
                from . import registry_key_evidence
                return registry_key_evidence.RegistryKeyEvidence()
            if mapping_value == '#microsoft.graph.security.registryValueEvidence':
                from . import registry_value_evidence
                return registry_value_evidence.RegistryValueEvidence()
            if mapping_value == '#microsoft.graph.security.securityGroupEvidence':
                from . import security_group_evidence
                return security_group_evidence.SecurityGroupEvidence()
            if mapping_value == '#microsoft.graph.security.urlEvidence':
                from . import url_evidence
                return url_evidence.UrlEvidence()
            if mapping_value == '#microsoft.graph.security.userEvidence':
                from . import user_evidence
                return user_evidence.UserEvidence()
        return AlertEvidence()

    def get_field_deserializers(self) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from . import analyzed_message_evidence, cloud_application_evidence, device_evidence, evidence_remediation_status, evidence_role, evidence_verdict, file_evidence, ip_evidence, mailbox_evidence, mail_cluster_evidence, oauth_application_evidence, process_evidence, registry_key_evidence, registry_value_evidence, security_group_evidence, url_evidence, user_evidence
        fields: Dict[str, Callable[[Any], None]] = {'createdDateTime': lambda n: setattr(self, 'created_date_time', n.get_datetime_value()), '@odata.type': lambda n: setattr(self, 'odata_type', n.get_str_value()), 'remediationStatus': lambda n: setattr(self, 'remediation_status', n.get_enum_value(evidence_remediation_status.EvidenceRemediationStatus)), 'remediationStatusDetails': lambda n: setattr(self, 'remediation_status_details', n.get_str_value()), 'roles': lambda n: setattr(self, 'roles', n.get_collection_of_enum_values(evidence_role.EvidenceRole)), 'tags': lambda n: setattr(self, 'tags', n.get_collection_of_primitive_values(str)), 'verdict': lambda n: setattr(self, 'verdict', n.get_enum_value(evidence_verdict.EvidenceVerdict))}
        return fields

    @property
    def odata_type(self) -> Optional[str]:
        """
        Gets the @odata.type property value. The OdataType property
        Returns: Optional[str]
        """
        return self._odata_type

    @odata_type.setter
    def odata_type(self, value: Optional[str]=None) -> None:
        """
        Sets the @odata.type property value. The OdataType property
        Args:
            value: Value to set for the odata_type property.
        """
        self._odata_type = value

    @property
    def remediation_status(self) -> Optional[evidence_remediation_status.EvidenceRemediationStatus]:
        """
        Gets the remediationStatus property value. The remediationStatus property
        Returns: Optional[evidence_remediation_status.EvidenceRemediationStatus]
        """
        return self._remediation_status

    @remediation_status.setter
    def remediation_status(self, value: Optional[evidence_remediation_status.EvidenceRemediationStatus]=None) -> None:
        """
        Sets the remediationStatus property value. The remediationStatus property
        Args:
            value: Value to set for the remediation_status property.
        """
        self._remediation_status = value

    @property
    def remediation_status_details(self) -> Optional[str]:
        """
        Gets the remediationStatusDetails property value. Details about the remediation status.
        Returns: Optional[str]
        """
        return self._remediation_status_details

    @remediation_status_details.setter
    def remediation_status_details(self, value: Optional[str]=None) -> None:
        """
        Sets the remediationStatusDetails property value. Details about the remediation status.
        Args:
            value: Value to set for the remediation_status_details property.
        """
        self._remediation_status_details = value

    @property
    def roles(self) -> Optional[List[evidence_role.EvidenceRole]]:
        """
        Gets the roles property value. The role/s that an evidence entity represents in an alert, e.g., an IP address that is associated with an attacker will have the evidence role 'Attacker'.
        Returns: Optional[List[evidence_role.EvidenceRole]]
        """
        return self._roles

    @roles.setter
    def roles(self, value: Optional[List[evidence_role.EvidenceRole]]=None) -> None:
        """
        Sets the roles property value. The role/s that an evidence entity represents in an alert, e.g., an IP address that is associated with an attacker will have the evidence role 'Attacker'.
        Args:
            value: Value to set for the roles property.
        """
        self._roles = value

    def serialize(self, writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        Args:
            writer: Serialization writer to use to serialize this model
        """
        if writer is None:
            raise Exception('writer cannot be undefined')
        writer.write_datetime_value('createdDateTime', self.created_date_time)
        writer.write_str_value('@odata.type', self.odata_type)
        writer.write_enum_value('remediationStatus', self.remediation_status)
        writer.write_str_value('remediationStatusDetails', self.remediation_status_details)
        writer.write_enum_value('roles', self.roles)
        writer.write_collection_of_primitive_values('tags', self.tags)
        writer.write_enum_value('verdict', self.verdict)
        writer.write_additional_data_value(self.additional_data)

    @property
    def tags(self) -> Optional[List[str]]:
        """
        Gets the tags property value. Array of custom tags associated with an evidence instance, for example to denote a group of devices, high value assets, etc.
        Returns: Optional[List[str]]
        """
        return self._tags

    @tags.setter
    def tags(self, value: Optional[List[str]]=None) -> None:
        """
        Sets the tags property value. Array of custom tags associated with an evidence instance, for example to denote a group of devices, high value assets, etc.
        Args:
            value: Value to set for the tags property.
        """
        self._tags = value

    @property
    def verdict(self) -> Optional[evidence_verdict.EvidenceVerdict]:
        """
        Gets the verdict property value. The verdict property
        Returns: Optional[evidence_verdict.EvidenceVerdict]
        """
        return self._verdict

    @verdict.setter
    def verdict(self, value: Optional[evidence_verdict.EvidenceVerdict]=None) -> None:
        """
        Sets the verdict property value. The verdict property
        Args:
            value: Value to set for the verdict property.
        """
        self._verdict = value