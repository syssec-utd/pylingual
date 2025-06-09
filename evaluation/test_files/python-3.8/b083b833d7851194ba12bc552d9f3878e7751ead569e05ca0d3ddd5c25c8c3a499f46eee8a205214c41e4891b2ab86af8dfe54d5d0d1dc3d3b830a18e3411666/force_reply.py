import geezlibs
from geezlibs import raw
from ..object import Object

class ForceReply(Object):
    """Object used to force clients to show a reply interface.

    Upon receiving a message with this object, Telegram clients will display a reply interface to the user.

    This acts as if the user has selected the bot's message and tapped "Reply".
    This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to
    sacrifice privacy mode.

    Parameters:
        selective (``bool``, *optional*):
            Use this parameter if you want to force reply from specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.

        placeholder (``str``, *optional*):
            The placeholder to be shown in the input field when the reply is active; 1-64 characters.
    """

    def __init__(self, selective: bool=None, placeholder: str=None):
        super().__init__()
        self.selective = selective
        self.placeholder = placeholder

    @staticmethod
    def read(b):
        return ForceReply(selective=b.selective, placeholder=b.placeholder)

    async def write(self, _: 'geezlibs.Client'):
        return raw.types.ReplyKeyboardForceReply(single_use=True, selective=self.selective or None, placeholder=self.placeholder or None)