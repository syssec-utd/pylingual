def gcm_send_message(registration_id, data, encoding='utf-8', **kwargs):
    """
    Standalone method to send a single gcm notification
    """
    messenger = GCMMessenger(registration_id, data, encoding=encoding, **kwargs)
    return messenger.send_plain()