def giving_up(self, message):
    """
        Called when a message has been received where ``msg.attempts > max_tries``

        This is useful to subclass and override to perform a task (such as writing to disk, etc.)

        :param message: the :class:`nsq.Message` received
        """
    logger.warning('[%s] giving up on message %s after %d tries (max:%d) %r', self.name, message.id, message.attempts, self.max_tries, message.body)