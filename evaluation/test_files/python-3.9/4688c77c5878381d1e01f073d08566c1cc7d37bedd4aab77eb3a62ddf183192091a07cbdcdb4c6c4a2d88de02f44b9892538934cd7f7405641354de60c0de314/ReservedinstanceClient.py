from jdcloud_sdk.core.jdcloudclient import JDCloudClient
from jdcloud_sdk.core.config import Config

class ReservedinstanceClient(JDCloudClient):

    def __init__(self, credential, config=None, logger=None):
        if config is None:
            config = Config('reservedinstance.jdcloud-api.com')
        super(ReservedinstanceClient, self).__init__(credential, config, 'reservedinstance', '0.1.2', logger)