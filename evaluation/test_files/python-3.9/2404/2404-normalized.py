def models(cls, api_version=DEFAULT_API_VERSION):
    """Module depends on the API version:

           * 2015-06-15: :mod:`v2015_06_15.models<azure.mgmt.compute.v2015_06_15.models>`
           * 2016-03-30: :mod:`v2016_03_30.models<azure.mgmt.compute.v2016_03_30.models>`
           * 2016-04-30-preview: :mod:`v2016_04_30_preview.models<azure.mgmt.compute.v2016_04_30_preview.models>`
           * 2017-03-30: :mod:`v2017_03_30.models<azure.mgmt.compute.v2017_03_30.models>`
           * 2017-09-01: :mod:`v2017_09_01.models<azure.mgmt.compute.v2017_09_01.models>`
           * 2017-12-01: :mod:`v2017_12_01.models<azure.mgmt.compute.v2017_12_01.models>`
           * 2018-04-01: :mod:`v2018_04_01.models<azure.mgmt.compute.v2018_04_01.models>`
           * 2018-06-01: :mod:`v2018_06_01.models<azure.mgmt.compute.v2018_06_01.models>`
           * 2018-09-30: :mod:`v2018_09_30.models<azure.mgmt.compute.v2018_09_30.models>`
           * 2018-10-01: :mod:`v2018_10_01.models<azure.mgmt.compute.v2018_10_01.models>`
           * 2019-03-01: :mod:`v2019_03_01.models<azure.mgmt.compute.v2019_03_01.models>`
           * 2019-04-01: :mod:`v2019_04_01.models<azure.mgmt.compute.v2019_04_01.models>`
        """
    if api_version == '2015-06-15':
        from .v2015_06_15 import models
        return models
    elif api_version == '2016-03-30':
        from .v2016_03_30 import models
        return models
    elif api_version == '2016-04-30-preview':
        from .v2016_04_30_preview import models
        return models
    elif api_version == '2017-03-30':
        from .v2017_03_30 import models
        return models
    elif api_version == '2017-09-01':
        from .v2017_09_01 import models
        return models
    elif api_version == '2017-12-01':
        from .v2017_12_01 import models
        return models
    elif api_version == '2018-04-01':
        from .v2018_04_01 import models
        return models
    elif api_version == '2018-06-01':
        from .v2018_06_01 import models
        return models
    elif api_version == '2018-09-30':
        from .v2018_09_30 import models
        return models
    elif api_version == '2018-10-01':
        from .v2018_10_01 import models
        return models
    elif api_version == '2019-03-01':
        from .v2019_03_01 import models
        return models
    elif api_version == '2019-04-01':
        from .v2019_04_01 import models
        return models
    raise NotImplementedError('APIVersion {} is not available'.format(api_version))