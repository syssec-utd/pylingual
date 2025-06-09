import proto
__protobuf__ = proto.module(package='google.ads.googleads.v12.resources', marshal='google.ads.googleads.v12', manifest={'UserLocationView'})

class UserLocationView(proto.Message):
    """A user location view.
    User Location View includes all metrics aggregated at the
    country level, one row per country. It reports metrics at the
    actual physical location of the user by targeted or not targeted
    location. If other segment fields are used, you may get more
    than one row per country.

    Attributes:
        resource_name (str):
            Output only. The resource name of the user location view.
            UserLocation view resource names have the form:

            ``customers/{customer_id}/userLocationViews/{country_criterion_id}~{targeting_location}``
        country_criterion_id (int):
            Output only. Criterion Id for the country.

            This field is a member of `oneof`_ ``_country_criterion_id``.
        targeting_location (bool):
            Output only. Indicates whether location was
            targeted or not.

            This field is a member of `oneof`_ ``_targeting_location``.
    """
    resource_name = proto.Field(proto.STRING, number=1)
    country_criterion_id = proto.Field(proto.INT64, number=4, optional=True)
    targeting_location = proto.Field(proto.BOOL, number=5, optional=True)
__all__ = tuple(sorted(__protobuf__.manifest))