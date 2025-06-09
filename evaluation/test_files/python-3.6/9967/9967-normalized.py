def get_user_groups(self, dn, group_search_dn=None, _connection=None):
    """
        Gets a list of groups a user at dn is a member of

        Args:
            dn (str): The dn of the user to find memberships for.
            _connection (ldap3.Connection): A connection object to use when
                searching. If not given, a temporary connection will be
                created, and destroyed after use.
            group_search_dn (str): The search dn for groups. Defaults to
                ``'{LDAP_GROUP_DN},{LDAP_BASE_DN}'``.

        Returns:
            list: A list of LDAP groups the user is a member of.
        """
    connection = _connection
    if not connection:
        connection = self._make_connection(bind_user=self.config.get('LDAP_BIND_USER_DN'), bind_password=self.config.get('LDAP_BIND_USER_PASSWORD'))
        connection.bind()
    safe_dn = ldap3.utils.conv.escape_filter_chars(dn)
    search_filter = '(&{group_filter}({members_attr}={user_dn}))'.format(group_filter=self.config.get('LDAP_GROUP_OBJECT_FILTER'), members_attr=self.config.get('LDAP_GROUP_MEMBERS_ATTR'), user_dn=safe_dn)
    log.debug("Searching for groups for specific user with filter '{0}' , base '{1}' and scope '{2}'".format(search_filter, group_search_dn or self.full_group_search_dn, self.config.get('LDAP_GROUP_SEARCH_SCOPE')))
    connection.search(search_base=group_search_dn or self.full_group_search_dn, search_filter=search_filter, attributes=self.config.get('LDAP_GET_GROUP_ATTRIBUTES'), search_scope=getattr(ldap3, self.config.get('LDAP_GROUP_SEARCH_SCOPE')))
    results = []
    for item in connection.response:
        if 'type' not in item or item.get('type') != 'searchResEntry':
            continue
        group_data = item['attributes']
        group_data['dn'] = item['dn']
        results.append(group_data)
    if not _connection:
        self.destroy_connection(connection)
    return results