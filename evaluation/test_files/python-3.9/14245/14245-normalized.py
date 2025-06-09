def remove_tier(self, name_num):
    """Remove a tier, when multiple tiers exist with that name only the
        first is removed.

        :param name_num: Name or number of the tier to remove.
        :type name_num: int or str
        :raises IndexError: If there is no tier with that number.
        """
    if isinstance(name_num, int):
        del self.tiers[name_num - 1]
    else:
        self.tiers = [i for i in self.tiers if i.name != name_num]