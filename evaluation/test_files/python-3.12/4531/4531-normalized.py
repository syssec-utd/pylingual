def prepare(self):
    """Prepare for monitoring - install agents etc"""
    agent_configs = []
    if self.config:
        agent_configs = self.config_manager.getconfig(self.config, self.default_target)
    for config in agent_configs:
        if config['host'] in ['localhost', '127.0.0.1', '::1']:
            client = self.clients['localhost'](config, self.old_style_configs, kill_old=self.kill_old)
        else:
            client = self.clients['ssh'](config, self.old_style_configs, timeout=5, kill_old=self.kill_old)
        logger.debug('Installing monitoring agent. Host: %s', client.host)
        agent_config, startup_config, customs_script = client.install()
        if agent_config:
            self.agents.append(client)
            self.artifact_files.append(agent_config)
        if startup_config:
            self.artifact_files.append(startup_config)
        if customs_script:
            self.artifact_files.append(customs_script)