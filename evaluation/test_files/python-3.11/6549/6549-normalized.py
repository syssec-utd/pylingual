def execute(self, device):
    """Execute a device. Used if the time between executions is greater than DEFAULT_DELAY

        :param scapy.packet.Packet device: Scapy packet
        :return: None
        """
    src = device.src.lower()
    device = self.devices[src]
    threading.Thread(target=device.execute, kwargs={'root_allowed': self.root_allowed}).start()