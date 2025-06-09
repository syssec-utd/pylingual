import proto
__protobuf__ = proto.module(package='google.ads.googleads.v12.enums', marshal='google.ads.googleads.v12', manifest={'FeedItemStatusEnum'})

class FeedItemStatusEnum(proto.Message):
    """Container for enum describing possible statuses of a feed
    item.

    """

    class FeedItemStatus(proto.Enum):
        """Possible statuses of a feed item."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        REMOVED = 3
__all__ = tuple(sorted(__protobuf__.manifest))