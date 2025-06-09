def create_affinity_group(self, name, label, location, description=None):
    """
        Creates a new affinity group for the specified subscription.

        name:
            A name for the affinity group that is unique to the subscription.
        label:
            A name for the affinity group. The name can be up to 100 characters
            in length.
        location:
            The data center location where the affinity group will be created.
            To list available locations, use the list_location function.
        description:
            A description for the affinity group. The description can be up to
            1024 characters in length.
        """
    _validate_not_none('name', name)
    _validate_not_none('label', label)
    _validate_not_none('location', location)
    return self._perform_post('/' + self.subscription_id + '/affinitygroups', _XmlSerializer.create_affinity_group_to_xml(name, label, description, location))