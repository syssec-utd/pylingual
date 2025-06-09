def remove_point(self, time):
    """Remove a point, if no point is found nothing happens.

        :param int time: Time of the point.
        :raises TierTypeException: If the tier is not a TextTier.
        """
    if self.tier_type != 'TextTier':
        raise Exception('Tiertype must be TextTier.')
    self.intervals = [i for i in self.intervals if i[0] != time]