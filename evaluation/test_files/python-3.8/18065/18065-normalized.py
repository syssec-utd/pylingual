def reject(self, pn_condition=None):
    """See Link Reject, AMQP1.0 spec."""
    self._pn_link.target.type = proton.Terminus.UNSPECIFIED
    super(ReceiverLink, self).reject(pn_condition)