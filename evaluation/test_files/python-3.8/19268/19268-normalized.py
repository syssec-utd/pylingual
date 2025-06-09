def turn_on_switch(self, device_id, name):
    """Create the message to turn switch on."""
    msg = '!%sF1|Turn On|%s' % (device_id, name)
    self._send_message(msg)