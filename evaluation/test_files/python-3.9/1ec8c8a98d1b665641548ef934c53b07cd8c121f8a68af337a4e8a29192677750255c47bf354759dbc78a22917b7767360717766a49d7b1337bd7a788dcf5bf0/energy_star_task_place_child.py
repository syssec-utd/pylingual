from msrest.serialization import Model

class EnergyStarTaskPlaceChild(Model):
    """EnergyStarTaskPlaceChild.

    :param building:
    :type building: ~energycap.sdk.models.PlaceChild
    :param task_periods: The list of submission or metrics periods for the
     task
    :type task_periods: list[~energycap.sdk.models.NamedPeriod]
    """
    _attribute_map = {'building': {'key': 'building', 'type': 'PlaceChild'}, 'task_periods': {'key': 'taskPeriods', 'type': '[NamedPeriod]'}}

    def __init__(self, **kwargs):
        super(EnergyStarTaskPlaceChild, self).__init__(**kwargs)
        self.building = kwargs.get('building', None)
        self.task_periods = kwargs.get('task_periods', None)