def get_annotation_data_after_time(self, id_tier, time):
    """Give the annotation before a given time. When the tier contains
        reference annotations this will be returned, check
        :func:`get_ref_annotation_data_before_time` for the format. If an
        annotation overlaps with ``time`` that annotation will be returned.

        :param str id_tier: Name of the tier.
        :param int time: Time to get the annotation before.
        :raises KeyError: If the tier is non existent.
        """
    if self.tiers[id_tier][1]:
        return self.get_ref_annotation_after_time(id_tier, time)
    befores = self.get_annotation_data_between_times(id_tier, time, self.get_full_time_interval()[1])
    if befores:
        return [min(befores, key=lambda x: x[0])]
    else:
        return []