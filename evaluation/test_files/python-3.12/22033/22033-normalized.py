def _set_kernel_manager(self, kernel_manager):
    """ Disconnect from the current kernel manager (if any) and set a new
            kernel manager.
        """
    old_manager = self._kernel_manager
    if old_manager is not None:
        old_manager.started_kernel.disconnect(self._started_kernel)
        old_manager.started_channels.disconnect(self._started_channels)
        old_manager.stopped_channels.disconnect(self._stopped_channels)
        old_manager.sub_channel.message_received.disconnect(self._dispatch)
        old_manager.shell_channel.message_received.disconnect(self._dispatch)
        old_manager.stdin_channel.message_received.disconnect(self._dispatch)
        old_manager.hb_channel.kernel_died.disconnect(self._handle_kernel_died)
        if old_manager.channels_running:
            self._stopped_channels()
    self._kernel_manager = kernel_manager
    if kernel_manager is None:
        return
    kernel_manager.started_kernel.connect(self._started_kernel)
    kernel_manager.started_channels.connect(self._started_channels)
    kernel_manager.stopped_channels.connect(self._stopped_channels)
    kernel_manager.sub_channel.message_received.connect(self._dispatch)
    kernel_manager.shell_channel.message_received.connect(self._dispatch)
    kernel_manager.stdin_channel.message_received.connect(self._dispatch)
    kernel_manager.hb_channel.kernel_died.connect(self._handle_kernel_died)
    if kernel_manager.channels_running:
        self._started_channels()