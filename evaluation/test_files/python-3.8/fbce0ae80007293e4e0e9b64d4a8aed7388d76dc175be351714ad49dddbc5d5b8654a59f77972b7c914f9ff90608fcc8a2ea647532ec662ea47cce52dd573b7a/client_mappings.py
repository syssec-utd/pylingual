import oci
from oci_cli.cli_clients import CLIENT_MAP
from oci_cli.cli_clients import MODULE_TO_TYPE_MAPPINGS
from oci.tenant_manager_control_plane import RecipientInvitationClient
MODULE_TO_TYPE_MAPPINGS['tenant_manager_control_plane'] = oci.tenant_manager_control_plane.models.tenant_manager_control_plane_type_mapping
if CLIENT_MAP.get('tenant_manager_control_plane') is None:
    CLIENT_MAP['tenant_manager_control_plane'] = {}
CLIENT_MAP['tenant_manager_control_plane']['recipient_invitation'] = RecipientInvitationClient