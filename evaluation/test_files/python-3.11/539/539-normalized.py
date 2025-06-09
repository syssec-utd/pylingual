def _prepare_cli_cmd(self):
    """
        This function creates the command list from available information
        """
    conn = self.conn
    hive_bin = 'hive'
    cmd_extra = []
    if self.use_beeline:
        hive_bin = 'beeline'
        jdbc_url = 'jdbc:hive2://{host}:{port}/{schema}'.format(host=conn.host, port=conn.port, schema=conn.schema)
        if configuration.conf.get('core', 'security') == 'kerberos':
            template = conn.extra_dejson.get('principal', 'hive/_HOST@EXAMPLE.COM')
            if '_HOST' in template:
                template = utils.replace_hostname_pattern(utils.get_components(template))
            proxy_user = ''
            if conn.extra_dejson.get('proxy_user') == 'login' and conn.login:
                proxy_user = 'hive.server2.proxy.user={0}'.format(conn.login)
            elif conn.extra_dejson.get('proxy_user') == 'owner' and self.run_as:
                proxy_user = 'hive.server2.proxy.user={0}'.format(self.run_as)
            jdbc_url += ';principal={template};{proxy_user}'.format(template=template, proxy_user=proxy_user)
        elif self.auth:
            jdbc_url += ';auth=' + self.auth
        jdbc_url = '"{}"'.format(jdbc_url)
        cmd_extra += ['-u', jdbc_url]
        if conn.login:
            cmd_extra += ['-n', conn.login]
        if conn.password:
            cmd_extra += ['-p', conn.password]
    hive_params_list = self.hive_cli_params.split()
    return [hive_bin] + cmd_extra + hive_params_list