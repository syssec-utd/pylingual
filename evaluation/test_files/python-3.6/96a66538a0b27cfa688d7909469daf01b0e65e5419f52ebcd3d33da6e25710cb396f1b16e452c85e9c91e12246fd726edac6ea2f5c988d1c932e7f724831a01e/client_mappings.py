import oci
from oci_cli.cli_clients import CLIENT_MAP
from oci_cli.cli_clients import MODULE_TO_TYPE_MAPPINGS
from oci.functions import FunctionsManagementClient
MODULE_TO_TYPE_MAPPINGS['functions'] = oci.functions.models.functions_type_mapping
if CLIENT_MAP.get('functions') is None:
    CLIENT_MAP['functions'] = {}
CLIENT_MAP['functions']['functions_management'] = FunctionsManagementClient