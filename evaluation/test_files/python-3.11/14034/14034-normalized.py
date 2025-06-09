def _get_logger_for_instance(self, instance: typing.Any) -> logging.Logger:
    """Get logger for log calls.

        :param instance: Owner class instance. Filled only if instance created, else None.
        :type instance: typing.Optional[owner]
        :return: logger instance
        :rtype: logging.Logger
        """
    if self.logger is not None:
        return self.logger
    elif hasattr(instance, 'logger') and isinstance(instance.logger, logging.Logger):
        return instance.logger
    elif hasattr(instance, 'log') and isinstance(instance.log, logging.Logger):
        return instance.log
    return _LOGGER