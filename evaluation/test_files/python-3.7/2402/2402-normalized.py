def abandon(self):
    """Abandon the message.

        This message will be returned to the queue to be reprocessed.

        :raises: ~azure.servicebus.common.errors.MessageAlreadySettled if the message has been settled.
        :raises: ~azure.servicebus.common.errors.MessageLockExpired if message lock has already expired.
        :raises: ~azure.servicebus.common.errors.SessionLockExpired if session lock has already expired.
        :raises: ~azure.servicebus.common.errors.MessageSettleFailed if message settle operation fails.
        """
    self._is_live('abandon')
    self._receiver._settle_deferred('abandoned', [self.lock_token])
    self._settled = True