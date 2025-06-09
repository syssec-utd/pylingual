def __detect_configuration(self):
    """
        we need to be flexible in order to determine which plugin's configuration
        specified and make appropriate configs to metrics collector

        :return: SECTION name or None for defaults
        """
    try:
        is_telegraf = self.core.get_option('telegraf', 'config')
    except KeyError:
        is_telegraf = None
    try:
        is_monitoring = self.core.get_option('monitoring', 'config')
    except KeyError:
        is_monitoring = None
    if is_telegraf and is_monitoring:
        raise ValueError('Both telegraf and monitoring configs specified. Clean up your config and delete one of them')
    if is_telegraf and (not is_monitoring):
        return 'telegraf'
    if not is_telegraf and is_monitoring:
        return 'monitoring'
    if not is_telegraf and (not is_monitoring):
        try:
            is_telegraf_dt = self.core.get_option('telegraf')
        except NoOptionError:
            is_telegraf_dt = None
        try:
            is_monitoring_dt = self.core.get_option('monitoring')
        except BaseException:
            is_monitoring_dt = None
        if is_telegraf_dt and is_monitoring_dt:
            raise ValueError('Both telegraf and monitoring default targets specified. Clean up your config and delete one of them')
        if is_telegraf_dt and (not is_monitoring_dt):
            return
        if not is_telegraf_dt and is_monitoring_dt:
            self.core.set_option('telegraf', 'default_target', is_monitoring_dt)
        if not is_telegraf_dt and (not is_monitoring_dt):
            return