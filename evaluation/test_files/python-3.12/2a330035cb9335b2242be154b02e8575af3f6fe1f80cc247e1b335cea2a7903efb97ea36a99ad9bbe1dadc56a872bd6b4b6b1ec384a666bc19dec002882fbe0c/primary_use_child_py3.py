from msrest.serialization import Model

class PrimaryUseChild(Model):
    """PrimaryUseChild.

    :param primary_use_id:
    :type primary_use_id: int
    :param primary_use_code:
    :type primary_use_code: str
    :param primary_use_info:
    :type primary_use_info: str
    """
    _attribute_map = {'primary_use_id': {'key': 'primaryUseId', 'type': 'int'}, 'primary_use_code': {'key': 'primaryUseCode', 'type': 'str'}, 'primary_use_info': {'key': 'primaryUseInfo', 'type': 'str'}}

    def __init__(self, *, primary_use_id: int=None, primary_use_code: str=None, primary_use_info: str=None, **kwargs) -> None:
        super(PrimaryUseChild, self).__init__(**kwargs)
        self.primary_use_id = primary_use_id
        self.primary_use_code = primary_use_code
        self.primary_use_info = primary_use_info