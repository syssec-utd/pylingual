import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['Endpoints']

@pulumi.output_type
class Endpoints(dict):

    def __init__(__self__, *, apps: Optional[str]=None, apps_rules: Optional[str]=None, auth_servers: Optional[str]=None, privileges: Optional[str]=None, risk_rules: Optional[str]=None, roles: Optional[str]=None, users: Optional[str]=None, users_v1: Optional[str]=None):
        if apps is not None:
            pulumi.set(__self__, 'apps', apps)
        if apps_rules is not None:
            pulumi.set(__self__, 'apps_rules', apps_rules)
        if auth_servers is not None:
            pulumi.set(__self__, 'auth_servers', auth_servers)
        if privileges is not None:
            pulumi.set(__self__, 'privileges', privileges)
        if risk_rules is not None:
            pulumi.set(__self__, 'risk_rules', risk_rules)
        if roles is not None:
            pulumi.set(__self__, 'roles', roles)
        if users is not None:
            pulumi.set(__self__, 'users', users)
        if users_v1 is not None:
            pulumi.set(__self__, 'users_v1', users_v1)

    @property
    @pulumi.getter
    def apps(self) -> Optional[str]:
        return pulumi.get(self, 'apps')

    @property
    @pulumi.getter(name='appsRules')
    def apps_rules(self) -> Optional[str]:
        return pulumi.get(self, 'apps_rules')

    @property
    @pulumi.getter(name='authServers')
    def auth_servers(self) -> Optional[str]:
        return pulumi.get(self, 'auth_servers')

    @property
    @pulumi.getter
    def privileges(self) -> Optional[str]:
        return pulumi.get(self, 'privileges')

    @property
    @pulumi.getter(name='riskRules')
    def risk_rules(self) -> Optional[str]:
        return pulumi.get(self, 'risk_rules')

    @property
    @pulumi.getter
    def roles(self) -> Optional[str]:
        return pulumi.get(self, 'roles')

    @property
    @pulumi.getter
    def users(self) -> Optional[str]:
        return pulumi.get(self, 'users')

    @property
    @pulumi.getter(name='usersV1')
    def users_v1(self) -> Optional[str]:
        return pulumi.get(self, 'users_v1')