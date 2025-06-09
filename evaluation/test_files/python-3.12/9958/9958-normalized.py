def init_config(self, config):
    """
        Configures this extension with a given configuration dictionary.
        This allows use of this extension without a flask app.

        Args:
            config (dict): A dictionary with configuration keys
        """
    self.config.update(config)
    self.config.setdefault('LDAP_PORT', 389)
    self.config.setdefault('LDAP_HOST', None)
    self.config.setdefault('LDAP_USE_SSL', False)
    self.config.setdefault('LDAP_READONLY', True)
    self.config.setdefault('LDAP_CHECK_NAMES', True)
    self.config.setdefault('LDAP_BIND_DIRECT_CREDENTIALS', False)
    self.config.setdefault('LDAP_BIND_DIRECT_PREFIX', '')
    self.config.setdefault('LDAP_BIND_DIRECT_SUFFIX', '')
    self.config.setdefault('LDAP_BIND_DIRECT_GET_USER_INFO', True)
    self.config.setdefault('LDAP_ALWAYS_SEARCH_BIND', False)
    self.config.setdefault('LDAP_BASE_DN', '')
    self.config.setdefault('LDAP_BIND_USER_DN', None)
    self.config.setdefault('LDAP_BIND_USER_PASSWORD', None)
    self.config.setdefault('LDAP_SEARCH_FOR_GROUPS', True)
    self.config.setdefault('LDAP_FAIL_AUTH_ON_MULTIPLE_FOUND', False)
    self.config.setdefault('LDAP_USER_DN', '')
    self.config.setdefault('LDAP_GROUP_DN', '')
    self.config.setdefault('LDAP_BIND_AUTHENTICATION_TYPE', 'SIMPLE')
    self.config.setdefault('LDAP_USER_SEARCH_SCOPE', 'LEVEL')
    self.config.setdefault('LDAP_USER_OBJECT_FILTER', '(objectclass=person)')
    self.config.setdefault('LDAP_USER_LOGIN_ATTR', 'uid')
    self.config.setdefault('LDAP_USER_RDN_ATTR', 'uid')
    self.config.setdefault('LDAP_GET_USER_ATTRIBUTES', ldap3.ALL_ATTRIBUTES)
    self.config.setdefault('LDAP_GROUP_SEARCH_SCOPE', 'LEVEL')
    self.config.setdefault('LDAP_GROUP_OBJECT_FILTER', '(objectclass=group)')
    self.config.setdefault('LDAP_GROUP_MEMBERS_ATTR', 'uniqueMember')
    self.config.setdefault('LDAP_GET_GROUP_ATTRIBUTES', ldap3.ALL_ATTRIBUTES)
    self.config.setdefault('LDAP_ADD_SERVER', True)
    if self.config['LDAP_ADD_SERVER']:
        self.add_server(hostname=self.config['LDAP_HOST'], port=self.config['LDAP_PORT'], use_ssl=self.config['LDAP_USE_SSL'])