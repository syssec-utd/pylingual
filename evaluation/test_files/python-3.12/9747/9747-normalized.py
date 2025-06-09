def connectInternSig(self):
    """
        connet signal from internal side of of this component to this port
        """
    d = self.direction
    if d == DIRECTION.OUT:
        self.src.endpoints.append(self)
    elif d == DIRECTION.IN or d == DIRECTION.INOUT:
        self.dst.drivers.append(self)
    else:
        raise NotImplementedError(d)