from th2_data_services.provider.v6.filters.filter import Provider6MessageFilter

class TypeFilter(Provider6MessageFilter):
    """Will match the messages by their full type name."""
    FILTER_NAME = 'type'

class BodyBinaryFilter(Provider6MessageFilter):
    """Will match the messages by their binary body."""
    FILTER_NAME = 'bodyBinary'

class BodyFilter(Provider6MessageFilter):
    """Will match the messages by their parsed body."""
    FILTER_NAME = 'body'

class AttachedEventIdsFilter(Provider6MessageFilter):
    """Filters the messages that are linked to the specified event id."""
    FILTER_NAME = 'attachedEventIds'