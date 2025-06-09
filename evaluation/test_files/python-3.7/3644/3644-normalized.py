def copy_to(self, context: 'TurnContext') -> None:
    """
        Called when this TurnContext instance is passed into the constructor of a new TurnContext
        instance. Can be overridden in derived classes.
        :param context:
        :return:
        """
    for attribute in ['adapter', 'activity', '_responded', '_services', '_on_send_activities', '_on_update_activity', '_on_delete_activity']:
        setattr(context, attribute, getattr(self, attribute))