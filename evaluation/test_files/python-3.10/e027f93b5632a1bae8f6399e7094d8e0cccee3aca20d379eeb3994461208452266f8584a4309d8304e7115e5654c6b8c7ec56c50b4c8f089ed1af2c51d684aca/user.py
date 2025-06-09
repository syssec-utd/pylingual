"""
@author: Nicklas Ansman-Giertz
@contact: U{ngiertz@splunk.com<mailto:ngiertz@splunk.com>}
@since: 2011-11-23
"""
from pytest_splunk_addon.helmut.manager.users.user import User

class SDKUserWrapper(User):
    """
    The L{User} subclass corresponding to an User object in the
    Splunk Python SDK.
    """

    def __init__(self, sdk_connector, sdk_user, username=None):
        """
        SDKUserWrapper's constructor.

        @param username: The name of the User which this object represents.
        @type username: String
        @param sdk_connector: The connector which talks to Splunk through the
                              Splunk Python SDK.
        @type sdk_connector: SDKConnector
        @param sdk_user: The splunklib.Entity which represent an User in the
                         Python SDK.
        """
        if username is None:
            username = sdk_user.name
        super(SDKUserWrapper, self).__init__(username, sdk_connector)
        self._raw_sdk_user = sdk_user

    @property
    def raw_sdk_user(self):
        return self._raw_sdk_user

    @property
    def _service(self):
        """
        Return the service associated with
        """
        return self.connector.service

    def full_name(self):
        return self.raw_sdk_user.content.realname