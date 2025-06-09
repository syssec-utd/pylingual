import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
__all__ = ['LdapSettingArgs', 'LdapSetting']

@pulumi.input_type
class LdapSettingArgs:

    def __init__(__self__, *, key: pulumi.Input[str], ldap_url: pulumi.Input[str], allow_user_to_access_profile: Optional[pulumi.Input[bool]]=None, auto_create_user: Optional[pulumi.Input[bool]]=None, email_attribute: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, ldap_poisoning_protection: Optional[pulumi.Input[bool]]=None, manager_dn: Optional[pulumi.Input[str]]=None, manager_password: Optional[pulumi.Input[str]]=None, paging_support_enabled: Optional[pulumi.Input[bool]]=None, search_base: Optional[pulumi.Input[str]]=None, search_filter: Optional[pulumi.Input[str]]=None, search_sub_tree: Optional[pulumi.Input[bool]]=None, user_dn_pattern: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a LdapSetting resource.
        :param pulumi.Input[str] key: The unique ID of the LDAP setting.
        :param pulumi.Input[str] ldap_url: Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        :param pulumi.Input[bool] allow_user_to_access_profile: When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        :param pulumi.Input[bool] auto_create_user: When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        :param pulumi.Input[str] email_attribute: An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
               - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        :param pulumi.Input[bool] enabled: When set, these settings are enabled. Default value is `true`.
        :param pulumi.Input[bool] ldap_poisoning_protection: Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        :param pulumi.Input[str] manager_dn: The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        :param pulumi.Input[str] manager_password: The password of the user binding to the LDAP server when using "search" authentication.
        :param pulumi.Input[bool] paging_support_enabled: When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        :param pulumi.Input[str] search_base: The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        :param pulumi.Input[str] search_filter: A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        :param pulumi.Input[bool] search_sub_tree: When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        :param pulumi.Input[str] user_dn_pattern: A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        pulumi.set(__self__, 'key', key)
        pulumi.set(__self__, 'ldap_url', ldap_url)
        if allow_user_to_access_profile is not None:
            pulumi.set(__self__, 'allow_user_to_access_profile', allow_user_to_access_profile)
        if auto_create_user is not None:
            pulumi.set(__self__, 'auto_create_user', auto_create_user)
        if email_attribute is not None:
            pulumi.set(__self__, 'email_attribute', email_attribute)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if ldap_poisoning_protection is not None:
            pulumi.set(__self__, 'ldap_poisoning_protection', ldap_poisoning_protection)
        if manager_dn is not None:
            pulumi.set(__self__, 'manager_dn', manager_dn)
        if manager_password is not None:
            pulumi.set(__self__, 'manager_password', manager_password)
        if paging_support_enabled is not None:
            pulumi.set(__self__, 'paging_support_enabled', paging_support_enabled)
        if search_base is not None:
            pulumi.set(__self__, 'search_base', search_base)
        if search_filter is not None:
            pulumi.set(__self__, 'search_filter', search_filter)
        if search_sub_tree is not None:
            pulumi.set(__self__, 'search_sub_tree', search_sub_tree)
        if user_dn_pattern is not None:
            pulumi.set(__self__, 'user_dn_pattern', user_dn_pattern)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The unique ID of the LDAP setting.
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter(name='ldapUrl')
    def ldap_url(self) -> pulumi.Input[str]:
        """
        Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        """
        return pulumi.get(self, 'ldap_url')

    @ldap_url.setter
    def ldap_url(self, value: pulumi.Input[str]):
        pulumi.set(self, 'ldap_url', value)

    @property
    @pulumi.getter(name='allowUserToAccessProfile')
    def allow_user_to_access_profile(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        """
        return pulumi.get(self, 'allow_user_to_access_profile')

    @allow_user_to_access_profile.setter
    def allow_user_to_access_profile(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'allow_user_to_access_profile', value)

    @property
    @pulumi.getter(name='autoCreateUser')
    def auto_create_user(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        """
        return pulumi.get(self, 'auto_create_user')

    @auto_create_user.setter
    def auto_create_user(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_create_user', value)

    @property
    @pulumi.getter(name='emailAttribute')
    def email_attribute(self) -> Optional[pulumi.Input[str]]:
        """
        An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
        - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        """
        return pulumi.get(self, 'email_attribute')

    @email_attribute.setter
    def email_attribute(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'email_attribute', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, these settings are enabled. Default value is `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter(name='ldapPoisoningProtection')
    def ldap_poisoning_protection(self) -> Optional[pulumi.Input[bool]]:
        """
        Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        """
        return pulumi.get(self, 'ldap_poisoning_protection')

    @ldap_poisoning_protection.setter
    def ldap_poisoning_protection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'ldap_poisoning_protection', value)

    @property
    @pulumi.getter(name='managerDn')
    def manager_dn(self) -> Optional[pulumi.Input[str]]:
        """
        The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        """
        return pulumi.get(self, 'manager_dn')

    @manager_dn.setter
    def manager_dn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'manager_dn', value)

    @property
    @pulumi.getter(name='managerPassword')
    def manager_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the user binding to the LDAP server when using "search" authentication.
        """
        return pulumi.get(self, 'manager_password')

    @manager_password.setter
    def manager_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'manager_password', value)

    @property
    @pulumi.getter(name='pagingSupportEnabled')
    def paging_support_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        """
        return pulumi.get(self, 'paging_support_enabled')

    @paging_support_enabled.setter
    def paging_support_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'paging_support_enabled', value)

    @property
    @pulumi.getter(name='searchBase')
    def search_base(self) -> Optional[pulumi.Input[str]]:
        """
        The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        """
        return pulumi.get(self, 'search_base')

    @search_base.setter
    def search_base(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'search_base', value)

    @property
    @pulumi.getter(name='searchFilter')
    def search_filter(self) -> Optional[pulumi.Input[str]]:
        """
        A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        """
        return pulumi.get(self, 'search_filter')

    @search_filter.setter
    def search_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'search_filter', value)

    @property
    @pulumi.getter(name='searchSubTree')
    def search_sub_tree(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        """
        return pulumi.get(self, 'search_sub_tree')

    @search_sub_tree.setter
    def search_sub_tree(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'search_sub_tree', value)

    @property
    @pulumi.getter(name='userDnPattern')
    def user_dn_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        return pulumi.get(self, 'user_dn_pattern')

    @user_dn_pattern.setter
    def user_dn_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_dn_pattern', value)

@pulumi.input_type
class _LdapSettingState:

    def __init__(__self__, *, allow_user_to_access_profile: Optional[pulumi.Input[bool]]=None, auto_create_user: Optional[pulumi.Input[bool]]=None, email_attribute: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, key: Optional[pulumi.Input[str]]=None, ldap_poisoning_protection: Optional[pulumi.Input[bool]]=None, ldap_url: Optional[pulumi.Input[str]]=None, manager_dn: Optional[pulumi.Input[str]]=None, manager_password: Optional[pulumi.Input[str]]=None, paging_support_enabled: Optional[pulumi.Input[bool]]=None, search_base: Optional[pulumi.Input[str]]=None, search_filter: Optional[pulumi.Input[str]]=None, search_sub_tree: Optional[pulumi.Input[bool]]=None, user_dn_pattern: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering LdapSetting resources.
        :param pulumi.Input[bool] allow_user_to_access_profile: When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        :param pulumi.Input[bool] auto_create_user: When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        :param pulumi.Input[str] email_attribute: An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
               - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        :param pulumi.Input[bool] enabled: When set, these settings are enabled. Default value is `true`.
        :param pulumi.Input[str] key: The unique ID of the LDAP setting.
        :param pulumi.Input[bool] ldap_poisoning_protection: Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        :param pulumi.Input[str] ldap_url: Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        :param pulumi.Input[str] manager_dn: The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        :param pulumi.Input[str] manager_password: The password of the user binding to the LDAP server when using "search" authentication.
        :param pulumi.Input[bool] paging_support_enabled: When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        :param pulumi.Input[str] search_base: The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        :param pulumi.Input[str] search_filter: A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        :param pulumi.Input[bool] search_sub_tree: When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        :param pulumi.Input[str] user_dn_pattern: A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        if allow_user_to_access_profile is not None:
            pulumi.set(__self__, 'allow_user_to_access_profile', allow_user_to_access_profile)
        if auto_create_user is not None:
            pulumi.set(__self__, 'auto_create_user', auto_create_user)
        if email_attribute is not None:
            pulumi.set(__self__, 'email_attribute', email_attribute)
        if enabled is not None:
            pulumi.set(__self__, 'enabled', enabled)
        if key is not None:
            pulumi.set(__self__, 'key', key)
        if ldap_poisoning_protection is not None:
            pulumi.set(__self__, 'ldap_poisoning_protection', ldap_poisoning_protection)
        if ldap_url is not None:
            pulumi.set(__self__, 'ldap_url', ldap_url)
        if manager_dn is not None:
            pulumi.set(__self__, 'manager_dn', manager_dn)
        if manager_password is not None:
            pulumi.set(__self__, 'manager_password', manager_password)
        if paging_support_enabled is not None:
            pulumi.set(__self__, 'paging_support_enabled', paging_support_enabled)
        if search_base is not None:
            pulumi.set(__self__, 'search_base', search_base)
        if search_filter is not None:
            pulumi.set(__self__, 'search_filter', search_filter)
        if search_sub_tree is not None:
            pulumi.set(__self__, 'search_sub_tree', search_sub_tree)
        if user_dn_pattern is not None:
            pulumi.set(__self__, 'user_dn_pattern', user_dn_pattern)

    @property
    @pulumi.getter(name='allowUserToAccessProfile')
    def allow_user_to_access_profile(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        """
        return pulumi.get(self, 'allow_user_to_access_profile')

    @allow_user_to_access_profile.setter
    def allow_user_to_access_profile(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'allow_user_to_access_profile', value)

    @property
    @pulumi.getter(name='autoCreateUser')
    def auto_create_user(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        """
        return pulumi.get(self, 'auto_create_user')

    @auto_create_user.setter
    def auto_create_user(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'auto_create_user', value)

    @property
    @pulumi.getter(name='emailAttribute')
    def email_attribute(self) -> Optional[pulumi.Input[str]]:
        """
        An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
        - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        """
        return pulumi.get(self, 'email_attribute')

    @email_attribute.setter
    def email_attribute(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'email_attribute', value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, these settings are enabled. Default value is `true`.
        """
        return pulumi.get(self, 'enabled')

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'enabled', value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        The unique ID of the LDAP setting.
        """
        return pulumi.get(self, 'key')

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'key', value)

    @property
    @pulumi.getter(name='ldapPoisoningProtection')
    def ldap_poisoning_protection(self) -> Optional[pulumi.Input[bool]]:
        """
        Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        """
        return pulumi.get(self, 'ldap_poisoning_protection')

    @ldap_poisoning_protection.setter
    def ldap_poisoning_protection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'ldap_poisoning_protection', value)

    @property
    @pulumi.getter(name='ldapUrl')
    def ldap_url(self) -> Optional[pulumi.Input[str]]:
        """
        Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        """
        return pulumi.get(self, 'ldap_url')

    @ldap_url.setter
    def ldap_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'ldap_url', value)

    @property
    @pulumi.getter(name='managerDn')
    def manager_dn(self) -> Optional[pulumi.Input[str]]:
        """
        The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        """
        return pulumi.get(self, 'manager_dn')

    @manager_dn.setter
    def manager_dn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'manager_dn', value)

    @property
    @pulumi.getter(name='managerPassword')
    def manager_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the user binding to the LDAP server when using "search" authentication.
        """
        return pulumi.get(self, 'manager_password')

    @manager_password.setter
    def manager_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'manager_password', value)

    @property
    @pulumi.getter(name='pagingSupportEnabled')
    def paging_support_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        """
        return pulumi.get(self, 'paging_support_enabled')

    @paging_support_enabled.setter
    def paging_support_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'paging_support_enabled', value)

    @property
    @pulumi.getter(name='searchBase')
    def search_base(self) -> Optional[pulumi.Input[str]]:
        """
        The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        """
        return pulumi.get(self, 'search_base')

    @search_base.setter
    def search_base(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'search_base', value)

    @property
    @pulumi.getter(name='searchFilter')
    def search_filter(self) -> Optional[pulumi.Input[str]]:
        """
        A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        """
        return pulumi.get(self, 'search_filter')

    @search_filter.setter
    def search_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'search_filter', value)

    @property
    @pulumi.getter(name='searchSubTree')
    def search_sub_tree(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        """
        return pulumi.get(self, 'search_sub_tree')

    @search_sub_tree.setter
    def search_sub_tree(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'search_sub_tree', value)

    @property
    @pulumi.getter(name='userDnPattern')
    def user_dn_pattern(self) -> Optional[pulumi.Input[str]]:
        """
        A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        return pulumi.get(self, 'user_dn_pattern')

    @user_dn_pattern.setter
    def user_dn_pattern(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'user_dn_pattern', value)

class LdapSetting(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, allow_user_to_access_profile: Optional[pulumi.Input[bool]]=None, auto_create_user: Optional[pulumi.Input[bool]]=None, email_attribute: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, key: Optional[pulumi.Input[str]]=None, ldap_poisoning_protection: Optional[pulumi.Input[bool]]=None, ldap_url: Optional[pulumi.Input[str]]=None, manager_dn: Optional[pulumi.Input[str]]=None, manager_password: Optional[pulumi.Input[str]]=None, paging_support_enabled: Optional[pulumi.Input[bool]]=None, search_base: Optional[pulumi.Input[str]]=None, search_filter: Optional[pulumi.Input[str]]=None, search_sub_tree: Optional[pulumi.Input[bool]]=None, user_dn_pattern: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        This resource can be used to manage Artifactory's LDAP settings for user authentication.

        When specified LDAP setting is active, Artifactory first attempts to authenticate the user against the LDAP server.
        If LDAP authentication fails, it then tries to authenticate via its internal database.

        ~>The `LdapSetting` resource utilizes endpoints which are blocked/removed in SaaS environments (i.e. in Artifactory online), rendering this resource incompatible with Artifactory SaaS environments.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_artifactory as artifactory

        # Configure Artifactory LDAP setting
        ldap_name = artifactory.LdapSetting("ldapName",
            allow_user_to_access_profile=False,
            auto_create_user=True,
            email_attribute="mail",
            enabled=True,
            key="ldap_name",
            ldap_poisoning_protection=True,
            ldap_url="ldap://ldap_server_url",
            manager_dn="mgr_dn",
            manager_password="mgr_passwd_random",
            paging_support_enabled=False,
            search_base="ou=users",
            search_filter="(uid={0})",
            search_sub_tree=True,
            user_dn_pattern="uid={0},ou=People")
        ```
        Note: `Key` argument has to match to the resource name.\\
        Reference Link: [JFrog LDAP](https://www.jfrog.com/confluence/display/JFROG/LDAP)

        ## Import

        LDAP setting can be imported using the key, e.g.

        ```sh
         $ pulumi import artifactory:index/ldapSetting:LdapSetting ldap_name ldap_name
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_user_to_access_profile: When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        :param pulumi.Input[bool] auto_create_user: When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        :param pulumi.Input[str] email_attribute: An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
               - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        :param pulumi.Input[bool] enabled: When set, these settings are enabled. Default value is `true`.
        :param pulumi.Input[str] key: The unique ID of the LDAP setting.
        :param pulumi.Input[bool] ldap_poisoning_protection: Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        :param pulumi.Input[str] ldap_url: Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        :param pulumi.Input[str] manager_dn: The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        :param pulumi.Input[str] manager_password: The password of the user binding to the LDAP server when using "search" authentication.
        :param pulumi.Input[bool] paging_support_enabled: When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        :param pulumi.Input[str] search_base: The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        :param pulumi.Input[str] search_filter: A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        :param pulumi.Input[bool] search_sub_tree: When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        :param pulumi.Input[str] user_dn_pattern: A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: LdapSettingArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        This resource can be used to manage Artifactory's LDAP settings for user authentication.

        When specified LDAP setting is active, Artifactory first attempts to authenticate the user against the LDAP server.
        If LDAP authentication fails, it then tries to authenticate via its internal database.

        ~>The `LdapSetting` resource utilizes endpoints which are blocked/removed in SaaS environments (i.e. in Artifactory online), rendering this resource incompatible with Artifactory SaaS environments.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_artifactory as artifactory

        # Configure Artifactory LDAP setting
        ldap_name = artifactory.LdapSetting("ldapName",
            allow_user_to_access_profile=False,
            auto_create_user=True,
            email_attribute="mail",
            enabled=True,
            key="ldap_name",
            ldap_poisoning_protection=True,
            ldap_url="ldap://ldap_server_url",
            manager_dn="mgr_dn",
            manager_password="mgr_passwd_random",
            paging_support_enabled=False,
            search_base="ou=users",
            search_filter="(uid={0})",
            search_sub_tree=True,
            user_dn_pattern="uid={0},ou=People")
        ```
        Note: `Key` argument has to match to the resource name.\\
        Reference Link: [JFrog LDAP](https://www.jfrog.com/confluence/display/JFROG/LDAP)

        ## Import

        LDAP setting can be imported using the key, e.g.

        ```sh
         $ pulumi import artifactory:index/ldapSetting:LdapSetting ldap_name ldap_name
        ```

        :param str resource_name: The name of the resource.
        :param LdapSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(LdapSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, allow_user_to_access_profile: Optional[pulumi.Input[bool]]=None, auto_create_user: Optional[pulumi.Input[bool]]=None, email_attribute: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, key: Optional[pulumi.Input[str]]=None, ldap_poisoning_protection: Optional[pulumi.Input[bool]]=None, ldap_url: Optional[pulumi.Input[str]]=None, manager_dn: Optional[pulumi.Input[str]]=None, manager_password: Optional[pulumi.Input[str]]=None, paging_support_enabled: Optional[pulumi.Input[bool]]=None, search_base: Optional[pulumi.Input[str]]=None, search_filter: Optional[pulumi.Input[str]]=None, search_sub_tree: Optional[pulumi.Input[bool]]=None, user_dn_pattern: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LdapSettingArgs.__new__(LdapSettingArgs)
            __props__.__dict__['allow_user_to_access_profile'] = allow_user_to_access_profile
            __props__.__dict__['auto_create_user'] = auto_create_user
            __props__.__dict__['email_attribute'] = email_attribute
            __props__.__dict__['enabled'] = enabled
            if key is None and (not opts.urn):
                raise TypeError("Missing required property 'key'")
            __props__.__dict__['key'] = key
            __props__.__dict__['ldap_poisoning_protection'] = ldap_poisoning_protection
            if ldap_url is None and (not opts.urn):
                raise TypeError("Missing required property 'ldap_url'")
            __props__.__dict__['ldap_url'] = ldap_url
            __props__.__dict__['manager_dn'] = manager_dn
            __props__.__dict__['manager_password'] = None if manager_password is None else pulumi.Output.secret(manager_password)
            __props__.__dict__['paging_support_enabled'] = paging_support_enabled
            __props__.__dict__['search_base'] = search_base
            __props__.__dict__['search_filter'] = search_filter
            __props__.__dict__['search_sub_tree'] = search_sub_tree
            __props__.__dict__['user_dn_pattern'] = user_dn_pattern
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=['managerPassword'])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(LdapSetting, __self__).__init__('artifactory:index/ldapSetting:LdapSetting', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, allow_user_to_access_profile: Optional[pulumi.Input[bool]]=None, auto_create_user: Optional[pulumi.Input[bool]]=None, email_attribute: Optional[pulumi.Input[str]]=None, enabled: Optional[pulumi.Input[bool]]=None, key: Optional[pulumi.Input[str]]=None, ldap_poisoning_protection: Optional[pulumi.Input[bool]]=None, ldap_url: Optional[pulumi.Input[str]]=None, manager_dn: Optional[pulumi.Input[str]]=None, manager_password: Optional[pulumi.Input[str]]=None, paging_support_enabled: Optional[pulumi.Input[bool]]=None, search_base: Optional[pulumi.Input[str]]=None, search_filter: Optional[pulumi.Input[str]]=None, search_sub_tree: Optional[pulumi.Input[bool]]=None, user_dn_pattern: Optional[pulumi.Input[str]]=None) -> 'LdapSetting':
        """
        Get an existing LdapSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_user_to_access_profile: When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        :param pulumi.Input[bool] auto_create_user: When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        :param pulumi.Input[str] email_attribute: An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
               - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        :param pulumi.Input[bool] enabled: When set, these settings are enabled. Default value is `true`.
        :param pulumi.Input[str] key: The unique ID of the LDAP setting.
        :param pulumi.Input[bool] ldap_poisoning_protection: Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        :param pulumi.Input[str] ldap_url: Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        :param pulumi.Input[str] manager_dn: The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        :param pulumi.Input[str] manager_password: The password of the user binding to the LDAP server when using "search" authentication.
        :param pulumi.Input[bool] paging_support_enabled: When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        :param pulumi.Input[str] search_base: The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        :param pulumi.Input[str] search_filter: A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        :param pulumi.Input[bool] search_sub_tree: When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        :param pulumi.Input[str] user_dn_pattern: A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
               - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _LdapSettingState.__new__(_LdapSettingState)
        __props__.__dict__['allow_user_to_access_profile'] = allow_user_to_access_profile
        __props__.__dict__['auto_create_user'] = auto_create_user
        __props__.__dict__['email_attribute'] = email_attribute
        __props__.__dict__['enabled'] = enabled
        __props__.__dict__['key'] = key
        __props__.__dict__['ldap_poisoning_protection'] = ldap_poisoning_protection
        __props__.__dict__['ldap_url'] = ldap_url
        __props__.__dict__['manager_dn'] = manager_dn
        __props__.__dict__['manager_password'] = manager_password
        __props__.__dict__['paging_support_enabled'] = paging_support_enabled
        __props__.__dict__['search_base'] = search_base
        __props__.__dict__['search_filter'] = search_filter
        __props__.__dict__['search_sub_tree'] = search_sub_tree
        __props__.__dict__['user_dn_pattern'] = user_dn_pattern
        return LdapSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='allowUserToAccessProfile')
    def allow_user_to_access_profile(self) -> pulumi.Output[Optional[bool]]:
        """
        When set, users created after logging in using LDAP will be able to access their profile page.  Default value is `false`.
        """
        return pulumi.get(self, 'allow_user_to_access_profile')

    @property
    @pulumi.getter(name='autoCreateUser')
    def auto_create_user(self) -> pulumi.Output[Optional[bool]]:
        """
        When set, the system will automatically create new users for those who have logged in using LDAP, and assign them to the default groups.  Default value is `true`.
        """
        return pulumi.get(self, 'auto_create_user')

    @property
    @pulumi.getter(name='emailAttribute')
    def email_attribute(self) -> pulumi.Output[Optional[str]]:
        """
        An attribute that can be used to map a user's email address to a user created automatically in Artifactory. Default value is `mail`.
        - Note: If blank/empty string input was set for email_attribute, Default value `mail` takes effect. This is to match with Artifactory behavior.
        """
        return pulumi.get(self, 'email_attribute')

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        When set, these settings are enabled. Default value is `true`.
        """
        return pulumi.get(self, 'enabled')

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        The unique ID of the LDAP setting.
        """
        return pulumi.get(self, 'key')

    @property
    @pulumi.getter(name='ldapPoisoningProtection')
    def ldap_poisoning_protection(self) -> pulumi.Output[Optional[bool]]:
        """
        Protects against LDAP poisoning by filtering out users exposed to vulnerabilities.  Default value is `true`.
        """
        return pulumi.get(self, 'ldap_poisoning_protection')

    @property
    @pulumi.getter(name='ldapUrl')
    def ldap_url(self) -> pulumi.Output[str]:
        """
        Location of the LDAP server in the following format: ldap://myserver:myport/dc=sampledomain,dc=com. The URL should include the base DN used to search for and/or authenticate users.
        """
        return pulumi.get(self, 'ldap_url')

    @property
    @pulumi.getter(name='managerDn')
    def manager_dn(self) -> pulumi.Output[Optional[str]]:
        """
        The full DN of a user with permissions that allow querying the LDAP server. When working with LDAP Groups, the user should have permissions for any extra group attributes such as memberOf.
        """
        return pulumi.get(self, 'manager_dn')

    @property
    @pulumi.getter(name='managerPassword')
    def manager_password(self) -> pulumi.Output[str]:
        """
        The password of the user binding to the LDAP server when using "search" authentication.
        """
        return pulumi.get(self, 'manager_password')

    @property
    @pulumi.getter(name='pagingSupportEnabled')
    def paging_support_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        When set, supports paging results for the LDAP server. This feature requires that the LDAP Server supports a PagedResultsControl configuration.  Default value is `true`.
        """
        return pulumi.get(self, 'paging_support_enabled')

    @property
    @pulumi.getter(name='searchBase')
    def search_base(self) -> pulumi.Output[Optional[str]]:
        """
        The Context name in which to search relative to the base DN in the LDAP URL. Multiple search bases may be specified separated by a pipe ( | ).
        """
        return pulumi.get(self, 'search_base')

    @property
    @pulumi.getter(name='searchFilter')
    def search_filter(self) -> pulumi.Output[Optional[str]]:
        """
        A filter expression used to search for the user DN that is used in LDAP authentication. This is an LDAP search filter (as defined in 'RFC 2254') with optional arguments. In this case, the username is the only argument, denoted by '{0}'. Possible examples are: uid={0}) - this would search for a username match on the uid attribute. Authentication using LDAP is performed from the DN found if successful. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both)
        """
        return pulumi.get(self, 'search_filter')

    @property
    @pulumi.getter(name='searchSubTree')
    def search_sub_tree(self) -> pulumi.Output[Optional[bool]]:
        """
        When set, enables deep search through the sub-tree of the LDAP URL + Search Base.  Default value is `true`.
        """
        return pulumi.get(self, 'search_sub_tree')

    @property
    @pulumi.getter(name='userDnPattern')
    def user_dn_pattern(self) -> pulumi.Output[Optional[str]]:
        """
        A DN pattern used to log users directly in to the LDAP database. This pattern is used to create a DN string for "direct" user authentication, and is relative to the base DN in the LDAP URL. The pattern argument {0} is replaced with the username at runtime. This only works if anonymous binding is allowed and a direct user DN can be used (which is not the default case for Active Directory). For example: uid={0},ou=People. Default value is blank/empty.
        - Note: LDAP settings should provide a userDnPattern or a searchFilter (or both).
        """
        return pulumi.get(self, 'user_dn_pattern')