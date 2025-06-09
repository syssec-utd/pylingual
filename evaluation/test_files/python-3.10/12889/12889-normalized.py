def receive_ack_requesting(self, pkt):
    """Receive ACK in REQUESTING state."""
    logger.debug('C3. Received ACK?, in REQUESTING state.')
    if self.process_received_ack(pkt):
        logger.debug('C3: T. Received ACK, in REQUESTING state, raise BOUND.')
        raise self.BOUND()