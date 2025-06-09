def to_eaf(self, skipempty=True, pointlength=0.1):
    """Convert the object to an pympi.Elan.Eaf object

        :param int pointlength: Length of respective interval from points in
                                seconds
        :param bool skipempty: Skip the empty annotations
        :returns: :class:`pympi.Elan.Eaf` object
        :raises ImportError: If the Eaf module can't be loaded.
        :raises ValueError: If the pointlength is not strictly positive.
        """
    from pympi.Elan import Eaf
    eaf_out = Eaf()
    if pointlength <= 0:
        raise ValueError('Pointlength should be strictly positive')
    for tier in self.get_tiers():
        eaf_out.add_tier(tier.name)
        for ann in tier.get_intervals(True):
            if tier.tier_type == 'TextTier':
                ann = (ann[0], ann[0] + pointlength, ann[1])
            if ann[2].strip() or not skipempty:
                eaf_out.add_annotation(tier.name, int(round(ann[0] * 1000)), int(round(ann[1] * 1000)), ann[2])
    return eaf_out