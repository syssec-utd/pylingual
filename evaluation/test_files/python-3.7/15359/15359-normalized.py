def _match_nodes(self, validators, obj):
    """Apply each validator in validators to each node in obj.

        Return each node in obj which matches all validators.
        """
    results = []
    for node in object_iter(obj):
        if all([validate(node) for validate in validators]):
            results.append(node)
    return results