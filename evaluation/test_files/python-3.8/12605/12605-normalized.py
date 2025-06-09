def add_parameters(self, traj):
    """Adds parameters and config from the `.ini` file to the trajectory"""
    if self.config_file:
        parameters = self._collect_section('parameters')
        for name in parameters:
            value = parameters[name]
            if not isinstance(value, tuple):
                value = (value,)
            traj.f_add_parameter(name, *value)
        config = self._collect_section('config')
        for name in config:
            value = config[name]
            if not isinstance(value, tuple):
                value = (value,)
            traj.f_add_config(name, *value)