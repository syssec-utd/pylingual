from __future__ import annotations
import datetime as dt
from dateutil import parser as dateparser
import pycallrail.base as base
import pycallrail.callrail as crl
import typing
import typing_extensions
import logging
import typeguard
from pycallrail.errors import LightValidationError

@typeguard.typechecked
class Company(base.CallRailBase):
    """
    Represents a Company.

    More information: https://apidocs.callrail.com/#companies
    """
    id: str
    name: str
    status: str
    time_zone: str
    created_at: dt.datetime
    disabled_at: typing.Optional[dt.datetime]
    dni_active: typing.Optional[bool]
    script_url: str
    callscore_enabled: bool
    lead_scoring_enabled: bool
    swap_exclude_jquery: typing.Optional[bool]
    ' Deprecated '
    swap_ppc_override: typing.Optional[bool]
    swap_landing_override: typing.Optional[str]
    swap_cookie_duration: typing.Optional[int]
    callscribe_enabled: bool
    keyword_spotting_enabled: typing.Optional[bool]
    ' Deprecated '
    form_capture: bool

    def __init__(self, api_client: crl.CallRail, account_id: str, **kwargs) -> None:
        super(Company, self).__init__()
        self.api_client: crl.CallRail = api_client
        self.account_id = account_id
        if not kwargs:
            raise TypeError(f'{self.__class__.__name__}() missing data arguments! Whats going on?')
        for k, v in kwargs.items():
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)

    @classmethod
    def from_json(cls, api_client: crl.CallRail, account_id: str, json_data: typing.Dict[str, typing.Any]) -> Company:
        """
        Deserialize a Company from a JSON object.
        
        :param api_client: The CallRail API client.
        :param account_id: The account ID.
        :param json_data: The JSON data.

        :return: A Company object.
        """
        json_data['disabled_at'] = dateparser.parse(json_data['disabled_at']) if json_data['disabled_at'] else None
        return cls(api_client, account_id, **json_data)

    def delete(self) -> None:
        """
        Delete the Company.
        """
        self.api_client._delete(endpoint=f'/a/{self.account_id}', path=f'/companies/{self.id}.json')

    def update(self, **kwargs) -> None:
        UPDATABLE_FIELDS: typing.List[str] = ['name', 'callscore_enabled', 'keyword_spotting_enabled', 'callscribe_enabled', 'time_zone', 'swap_exclude_jquery', 'swap_ppc_override', 'swap_landing_override', 'swap_cookie_duration', 'external_form_capture']
        body = {}
        for k, v in kwargs.items():
            if k not in UPDATABLE_FIELDS:
                raise LightValidationError(f'{k} is not updatable!')
            else:
                setattr(self, k, v)
                body[k] = v
        self.api_client._put(endpoint=f'/a/{self.account_id}', path=f'/companies/{self.id}.json', data=body)