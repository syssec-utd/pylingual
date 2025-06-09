import itertools
from datetime import datetime
from .main import AlphaDataclass, AlphaMappingAttribute, dataclass, field, List
from alphaz.libs import json_lib

@dataclass
class AlphaApplication(AlphaDataclass):
    id: int
    name: str
    description: str = None

@dataclass
class AlphaPermission(AlphaDataclass):
    key: str
    activated: bool
    description: str = None
    update_date: datetime = None

@dataclass
class AlphaRole(AlphaDataclass):
    name: str
    activated: bool
    id_app: int
    app: AlphaApplication
    description: str = None
    permissions: List[AlphaPermission] = field(default_factory=lambda: [])

@dataclass
class AlphaUserRole(AlphaDataclass):
    user_id: int
    role_name: str
    role: AlphaRole
    activated: bool

@dataclass
class AlphaUser(AlphaDataclass):
    id: int
    username: str
    last_activity: datetime = None
    mail: str = None
    role: int = -1
    password: str = None
    infos: dict = field(default_factory=lambda: {})
    roles: List[AlphaRole] = field(default_factory=lambda: [])
    permissions: List[str] = field(default_factory=lambda: [])
    registration_token: str = None
    pass_reset_token_exp: str = None
    registration_code: str = None
    expire: str = None
    telegram_id: str = None
    pass_reset_token: str = None
    date_registred: str = None

    def __post_init__(self):
        permissions = [[x.key for x in y.permissions if x is not None and x.activated] for y in self.roles if y is not None and y.activated]
        self.permissions = list(itertools.chain(*permissions))
        if type(self.infos) == dict:
            infos = json_lib.load_json(self.infos)
            infos = {x.decode('utf-8') if hasattr(x, 'decode') else x: y.decode('utf-8') if hasattr(y, 'decode') else y for x, y in infos.items()}
            self.infos = infos

    @classmethod
    def map_from_token(dataclass_type, token_dict):
        fields_names = dataclass_type.get_fields_names()
        corresp = {'sub': 'username'}
        return dataclass_type.map_from_dict({r: t for r, t in {corresp[x] if x in corresp else x: y for x, y in token_dict.items()}.items() if r in fields_names})

@dataclass
class AlphaUserSession(AlphaDataclass):
    user_id: int
    token: str
    ip: int
    expire: datetime
    update_date: datetime = None

@dataclass
class AlphaRolePermission(AlphaDataclass):
    role_name: str
    role: AlphaRole
    permission_key: str
    permission: AlphaPermission
    activated: bool