from dataclasses import dataclass
from typing import Literal, Optional, TYPE_CHECKING
from telebox.telegram_bot.types.type import Type
from telebox.telegram_bot.utils import get_url, get_full_name, get_chat_id_without_prefix
from telebox.telegram_bot.consts import chat_types
from telebox.telegram_bot.types.types.chat_photo import ChatPhoto
from telebox.telegram_bot.types.types.chat_permissions import ChatPermissions
from telebox.telegram_bot.types.types.chat_location import ChatLocation
if TYPE_CHECKING:
    from telebox.telegram_bot.types.types.message import Message

@dataclass(unsafe_hash=True)
class Chat(Type):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    bio: Optional[str] = None
    has_private_forwards: Optional[Literal[True]] = None
    has_restricted_voice_and_video_messages: Optional[Literal[True]] = None
    join_to_send_messages: Optional[Literal[True]] = None
    join_by_request: Optional[Literal[True]] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    pinned_message: Optional['Message'] = None
    permissions: Optional[ChatPermissions] = None
    slow_mode_delay: Optional[int] = None
    message_auto_delete_time: Optional[int] = None
    has_protected_content: Optional[Literal[True]] = None
    sticker_set_name: Optional[str] = None
    can_set_sticker_set: Optional[Literal[True]] = None
    linked_chat_id: Optional[int] = None
    location: Optional[ChatLocation] = None

    @property
    def id_without_prefix(self) -> int:
        if self.type in {chat_types.CHANNEL, chat_types.SUPERGROUP}:
            return get_chat_id_without_prefix(self.id)
        return self.id

    @property
    def full_name(self) -> Optional[str]:
        if self.first_name is not None:
            return get_full_name(self.first_name, self.last_name)

    @property
    def url(self) -> Optional[str]:
        if self.username is not None:
            return get_url(self.username)
        elif self.invite_link is not None:
            return self.invite_link