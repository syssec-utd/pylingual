from msrest.serialization import Model

class DashboardAndMapsModule(Model):
    """DashboardAndMapsModule.

    :param view:
    :type view: bool
    :param permission_id:
    :type permission_id: int
    :param permission_code:
    :type permission_code: str
    :param permission_name:
    :type permission_name: str
    :param description:
    :type description: str
    :param permission_category_name:
    :type permission_category_name: str
    :param is_licensed:
    :type is_licensed: bool
    """
    _attribute_map = {'view': {'key': 'view', 'type': 'bool'}, 'permission_id': {'key': 'permissionId', 'type': 'int'}, 'permission_code': {'key': 'permissionCode', 'type': 'str'}, 'permission_name': {'key': 'permissionName', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'permission_category_name': {'key': 'permissionCategoryName', 'type': 'str'}, 'is_licensed': {'key': 'isLicensed', 'type': 'bool'}}

    def __init__(self, *, view: bool=None, permission_id: int=None, permission_code: str=None, permission_name: str=None, description: str=None, permission_category_name: str=None, is_licensed: bool=None, **kwargs) -> None:
        super(DashboardAndMapsModule, self).__init__(**kwargs)
        self.view = view
        self.permission_id = permission_id
        self.permission_code = permission_code
        self.permission_name = permission_name
        self.description = description
        self.permission_category_name = permission_category_name
        self.is_licensed = is_licensed