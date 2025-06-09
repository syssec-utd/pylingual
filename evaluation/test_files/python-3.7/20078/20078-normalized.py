def disconnect(self, instance, another_instance):
    """
        Disconnect an *instance* from *another_instance*.
        """
    if instance not in self:
        return False
    if another_instance not in self[instance]:
        return False
    self[instance].remove(another_instance)
    return True