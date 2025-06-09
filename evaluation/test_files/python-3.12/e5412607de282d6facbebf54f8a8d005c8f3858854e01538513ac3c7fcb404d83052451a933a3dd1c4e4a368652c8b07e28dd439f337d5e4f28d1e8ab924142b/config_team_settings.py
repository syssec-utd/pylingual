from typing import Any, Dict, List, Type, TypeVar, Union
import attr
from ..types import UNSET, Unset
T = TypeVar('T', bound='ConfigTeamSettings')

@attr.s(auto_attribs=True)
class ConfigTeamSettings:
    """
    Attributes:
        site_name (Union[Unset, str]):
        max_users_per_team (Union[Unset, int]):
        enable_team_creation (Union[Unset, bool]):
        enable_user_creation (Union[Unset, bool]):
        enable_open_server (Union[Unset, bool]):
        restrict_creation_to_domains (Union[Unset, str]):
        enable_custom_brand (Union[Unset, bool]):
        custom_brand_text (Union[Unset, str]):
        custom_description_text (Union[Unset, str]):
        restrict_direct_message (Union[Unset, str]):
        restrict_team_invite (Union[Unset, str]):
        restrict_public_channel_management (Union[Unset, str]):
        restrict_private_channel_management (Union[Unset, str]):
        restrict_public_channel_creation (Union[Unset, str]):
        restrict_private_channel_creation (Union[Unset, str]):
        restrict_public_channel_deletion (Union[Unset, str]):
        restrict_private_channel_deletion (Union[Unset, str]):
        user_status_away_timeout (Union[Unset, int]):
        max_channels_per_team (Union[Unset, int]):
        max_notifications_per_channel (Union[Unset, int]):
    """
    site_name: Union[Unset, str] = UNSET
    max_users_per_team: Union[Unset, int] = UNSET
    enable_team_creation: Union[Unset, bool] = UNSET
    enable_user_creation: Union[Unset, bool] = UNSET
    enable_open_server: Union[Unset, bool] = UNSET
    restrict_creation_to_domains: Union[Unset, str] = UNSET
    enable_custom_brand: Union[Unset, bool] = UNSET
    custom_brand_text: Union[Unset, str] = UNSET
    custom_description_text: Union[Unset, str] = UNSET
    restrict_direct_message: Union[Unset, str] = UNSET
    restrict_team_invite: Union[Unset, str] = UNSET
    restrict_public_channel_management: Union[Unset, str] = UNSET
    restrict_private_channel_management: Union[Unset, str] = UNSET
    restrict_public_channel_creation: Union[Unset, str] = UNSET
    restrict_private_channel_creation: Union[Unset, str] = UNSET
    restrict_public_channel_deletion: Union[Unset, str] = UNSET
    restrict_private_channel_deletion: Union[Unset, str] = UNSET
    user_status_away_timeout: Union[Unset, int] = UNSET
    max_channels_per_team: Union[Unset, int] = UNSET
    max_notifications_per_channel: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        site_name = self.site_name
        max_users_per_team = self.max_users_per_team
        enable_team_creation = self.enable_team_creation
        enable_user_creation = self.enable_user_creation
        enable_open_server = self.enable_open_server
        restrict_creation_to_domains = self.restrict_creation_to_domains
        enable_custom_brand = self.enable_custom_brand
        custom_brand_text = self.custom_brand_text
        custom_description_text = self.custom_description_text
        restrict_direct_message = self.restrict_direct_message
        restrict_team_invite = self.restrict_team_invite
        restrict_public_channel_management = self.restrict_public_channel_management
        restrict_private_channel_management = self.restrict_private_channel_management
        restrict_public_channel_creation = self.restrict_public_channel_creation
        restrict_private_channel_creation = self.restrict_private_channel_creation
        restrict_public_channel_deletion = self.restrict_public_channel_deletion
        restrict_private_channel_deletion = self.restrict_private_channel_deletion
        user_status_away_timeout = self.user_status_away_timeout
        max_channels_per_team = self.max_channels_per_team
        max_notifications_per_channel = self.max_notifications_per_channel
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if site_name is not UNSET:
            field_dict['SiteName'] = site_name
        if max_users_per_team is not UNSET:
            field_dict['MaxUsersPerTeam'] = max_users_per_team
        if enable_team_creation is not UNSET:
            field_dict['EnableTeamCreation'] = enable_team_creation
        if enable_user_creation is not UNSET:
            field_dict['EnableUserCreation'] = enable_user_creation
        if enable_open_server is not UNSET:
            field_dict['EnableOpenServer'] = enable_open_server
        if restrict_creation_to_domains is not UNSET:
            field_dict['RestrictCreationToDomains'] = restrict_creation_to_domains
        if enable_custom_brand is not UNSET:
            field_dict['EnableCustomBrand'] = enable_custom_brand
        if custom_brand_text is not UNSET:
            field_dict['CustomBrandText'] = custom_brand_text
        if custom_description_text is not UNSET:
            field_dict['CustomDescriptionText'] = custom_description_text
        if restrict_direct_message is not UNSET:
            field_dict['RestrictDirectMessage'] = restrict_direct_message
        if restrict_team_invite is not UNSET:
            field_dict['RestrictTeamInvite'] = restrict_team_invite
        if restrict_public_channel_management is not UNSET:
            field_dict['RestrictPublicChannelManagement'] = restrict_public_channel_management
        if restrict_private_channel_management is not UNSET:
            field_dict['RestrictPrivateChannelManagement'] = restrict_private_channel_management
        if restrict_public_channel_creation is not UNSET:
            field_dict['RestrictPublicChannelCreation'] = restrict_public_channel_creation
        if restrict_private_channel_creation is not UNSET:
            field_dict['RestrictPrivateChannelCreation'] = restrict_private_channel_creation
        if restrict_public_channel_deletion is not UNSET:
            field_dict['RestrictPublicChannelDeletion'] = restrict_public_channel_deletion
        if restrict_private_channel_deletion is not UNSET:
            field_dict['RestrictPrivateChannelDeletion'] = restrict_private_channel_deletion
        if user_status_away_timeout is not UNSET:
            field_dict['UserStatusAwayTimeout'] = user_status_away_timeout
        if max_channels_per_team is not UNSET:
            field_dict['MaxChannelsPerTeam'] = max_channels_per_team
        if max_notifications_per_channel is not UNSET:
            field_dict['MaxNotificationsPerChannel'] = max_notifications_per_channel
        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        site_name = d.pop('SiteName', UNSET)
        max_users_per_team = d.pop('MaxUsersPerTeam', UNSET)
        enable_team_creation = d.pop('EnableTeamCreation', UNSET)
        enable_user_creation = d.pop('EnableUserCreation', UNSET)
        enable_open_server = d.pop('EnableOpenServer', UNSET)
        restrict_creation_to_domains = d.pop('RestrictCreationToDomains', UNSET)
        enable_custom_brand = d.pop('EnableCustomBrand', UNSET)
        custom_brand_text = d.pop('CustomBrandText', UNSET)
        custom_description_text = d.pop('CustomDescriptionText', UNSET)
        restrict_direct_message = d.pop('RestrictDirectMessage', UNSET)
        restrict_team_invite = d.pop('RestrictTeamInvite', UNSET)
        restrict_public_channel_management = d.pop('RestrictPublicChannelManagement', UNSET)
        restrict_private_channel_management = d.pop('RestrictPrivateChannelManagement', UNSET)
        restrict_public_channel_creation = d.pop('RestrictPublicChannelCreation', UNSET)
        restrict_private_channel_creation = d.pop('RestrictPrivateChannelCreation', UNSET)
        restrict_public_channel_deletion = d.pop('RestrictPublicChannelDeletion', UNSET)
        restrict_private_channel_deletion = d.pop('RestrictPrivateChannelDeletion', UNSET)
        user_status_away_timeout = d.pop('UserStatusAwayTimeout', UNSET)
        max_channels_per_team = d.pop('MaxChannelsPerTeam', UNSET)
        max_notifications_per_channel = d.pop('MaxNotificationsPerChannel', UNSET)
        config_team_settings = cls(site_name=site_name, max_users_per_team=max_users_per_team, enable_team_creation=enable_team_creation, enable_user_creation=enable_user_creation, enable_open_server=enable_open_server, restrict_creation_to_domains=restrict_creation_to_domains, enable_custom_brand=enable_custom_brand, custom_brand_text=custom_brand_text, custom_description_text=custom_description_text, restrict_direct_message=restrict_direct_message, restrict_team_invite=restrict_team_invite, restrict_public_channel_management=restrict_public_channel_management, restrict_private_channel_management=restrict_private_channel_management, restrict_public_channel_creation=restrict_public_channel_creation, restrict_private_channel_creation=restrict_private_channel_creation, restrict_public_channel_deletion=restrict_public_channel_deletion, restrict_private_channel_deletion=restrict_private_channel_deletion, user_status_away_timeout=user_status_away_timeout, max_channels_per_team=max_channels_per_team, max_notifications_per_channel=max_notifications_per_channel)
        config_team_settings.additional_properties = d
        return config_team_settings

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties