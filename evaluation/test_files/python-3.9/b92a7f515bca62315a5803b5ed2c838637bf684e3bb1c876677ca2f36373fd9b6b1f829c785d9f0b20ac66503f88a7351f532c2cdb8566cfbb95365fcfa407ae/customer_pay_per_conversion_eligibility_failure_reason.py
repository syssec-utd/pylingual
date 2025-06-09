import proto
__protobuf__ = proto.module(package='google.ads.googleads.v12.enums', marshal='google.ads.googleads.v12', manifest={'CustomerPayPerConversionEligibilityFailureReasonEnum'})

class CustomerPayPerConversionEligibilityFailureReasonEnum(proto.Message):
    """Container for enum describing reasons why a customer is not
    eligible to use PaymentMode.CONVERSIONS.

    """

    class CustomerPayPerConversionEligibilityFailureReason(proto.Enum):
        """Enum describing possible reasons a customer is not eligible
        to use PaymentMode.CONVERSIONS.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        NOT_ENOUGH_CONVERSIONS = 2
        CONVERSION_LAG_TOO_HIGH = 3
        HAS_CAMPAIGN_WITH_SHARED_BUDGET = 4
        HAS_UPLOAD_CLICKS_CONVERSION = 5
        AVERAGE_DAILY_SPEND_TOO_HIGH = 6
        ANALYSIS_NOT_COMPLETE = 7
        OTHER = 8
__all__ = tuple(sorted(__protobuf__.manifest))