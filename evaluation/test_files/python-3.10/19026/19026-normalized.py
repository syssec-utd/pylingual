def init_stage(self, name, config):
    """Construct and configure a stage from known stages.

        `name` must be the name of one of the stages in this.  `config`
        is the configuration dictionary of the containing object, and its `name`
        member will be passed into the stage constructor.

        :param str name: name of the stage
        :param dict config: parent object configuration
        :return: callable stage
        :raise exceptions.KeyError: if `name` is not a known stage

        """
    subconfig = config.get(name, {})
    ctor = self[name]
    return ctor(subconfig)