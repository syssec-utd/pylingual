import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['ActorResponse', 'CaseClassificationResponse']

@pulumi.output_type
class ActorResponse(dict):
    """
    An object containing information about the effective user and authenticated principal responsible for an action.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'displayName':
            suggest = 'display_name'
        elif key == 'googleSupport':
            suggest = 'google_support'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ActorResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ActorResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        ActorResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, display_name: str, email: str, google_support: bool):
        """
        An object containing information about the effective user and authenticated principal responsible for an action.
        :param str display_name: The name to display for the actor. If not provided, it is inferred from credentials supplied during case creation. When an email is provided, a display name must also be provided. This will be obfuscated if the user is a Google Support agent.
        :param str email: The email address of the actor. If not provided, it is inferred from credentials supplied during case creation. If the authenticated principal does not have an email address, one must be provided. When a name is provided, an email must also be provided. This will be obfuscated if the user is a Google Support agent.
        :param bool google_support: Whether the actor is a Google support actor.
        """
        pulumi.set(__self__, 'display_name', display_name)
        pulumi.set(__self__, 'email', email)
        pulumi.set(__self__, 'google_support', google_support)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        The name to display for the actor. If not provided, it is inferred from credentials supplied during case creation. When an email is provided, a display name must also be provided. This will be obfuscated if the user is a Google Support agent.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def email(self) -> str:
        """
        The email address of the actor. If not provided, it is inferred from credentials supplied during case creation. If the authenticated principal does not have an email address, one must be provided. When a name is provided, an email must also be provided. This will be obfuscated if the user is a Google Support agent.
        """
        return pulumi.get(self, 'email')

    @property
    @pulumi.getter(name='googleSupport')
    def google_support(self) -> bool:
        """
        Whether the actor is a Google support actor.
        """
        return pulumi.get(self, 'google_support')

@pulumi.output_type
class CaseClassificationResponse(dict):
    """
    A classification object with a product type and value.
    """

    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == 'displayName':
            suggest = 'display_name'
        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CaseClassificationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CaseClassificationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default=None) -> Any:
        CaseClassificationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *, display_name: str):
        """
        A classification object with a product type and value.
        :param str display_name: The display name of the classification.
        """
        pulumi.set(__self__, 'display_name', display_name)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> str:
        """
        The display name of the classification.
        """
        return pulumi.get(self, 'display_name')