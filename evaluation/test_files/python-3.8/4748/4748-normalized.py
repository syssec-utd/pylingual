def as_action_description(self):
    """
        Get the action description.

        Returns a dictionary describing the action.
        """
    description = {self.name: {'href': self.href_prefix + self.href, 'timeRequested': self.time_requested, 'status': self.status}}
    if self.input is not None:
        description[self.name]['input'] = self.input
    if self.time_completed is not None:
        description[self.name]['timeCompleted'] = self.time_completed
    return description