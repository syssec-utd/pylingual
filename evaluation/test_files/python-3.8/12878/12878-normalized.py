def INIT(self):
    """INIT state.

        [:rfc:`2131#section-4.4.1`]::

            The client SHOULD wait a random time between one and ten
            seconds to desynchronize the use of DHCP at startup

        .. todo::
           - The initial delay is implemented, but probably is not in other
             implementations. Check what other implementations do.
        """
    logger.debug('In state: INIT')
    if self.current_state is not STATE_PREINIT:
        self.reset()
    self.current_state = STATE_INIT
    if self.delay_selecting:
        if self.delay_before_selecting is None:
            delay_before_selecting = gen_delay_selecting()
        else:
            delay_before_selecting = self.delay_before_selecting
    else:
        delay_before_selecting = 0
    self.set_timeout(self.current_state, self.timeout_delay_before_selecting, delay_before_selecting)
    if self.timeout_select is not None:
        self.set_timeout(STATE_SELECTING, self.timeout_selecting, self.timeout_select)