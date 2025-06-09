def receive_offer(self, pkt):
    """Receive offer on SELECTING state."""
    logger.debug('C2. Received OFFER?, in SELECTING state.')
    if isoffer(pkt):
        logger.debug('C2: T, OFFER received')
        self.offers.append(pkt)
        if len(self.offers) >= MAX_OFFERS_COLLECTED:
            logger.debug('C2.5: T, raise REQUESTING.')
            self.select_offer()
            raise self.REQUESTING()
        logger.debug('C2.5: F, raise SELECTING.')
        raise self.SELECTING()