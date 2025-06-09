import proto
__protobuf__ = proto.module(package='google.ads.googleads.v12.enums', marshal='google.ads.googleads.v12', manifest={'ValueRuleDeviceTypeEnum'})

class ValueRuleDeviceTypeEnum(proto.Message):
    """Container for enum describing possible device types used in a
    conversion value rule.

    """

    class ValueRuleDeviceType(proto.Enum):
        """Possible device types used in conversion value rule."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        MOBILE = 2
        DESKTOP = 3
        TABLET = 4
__all__ = tuple(sorted(__protobuf__.manifest))