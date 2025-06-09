def cu3(self, theta, phi, lam, ctl, tgt):
    """Apply cu3 from ctl to tgt with angle theta, phi, lam."""
    return self.append(Cu3Gate(theta, phi, lam), [ctl, tgt], [])