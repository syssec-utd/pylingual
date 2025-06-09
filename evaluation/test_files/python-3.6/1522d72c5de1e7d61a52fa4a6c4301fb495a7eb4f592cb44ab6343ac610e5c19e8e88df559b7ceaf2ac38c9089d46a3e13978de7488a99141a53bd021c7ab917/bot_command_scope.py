import pyFipper
from pyFipper import raw
from ..object import Object

class BotCommandScope(Object):
    """Represents the scope to which bot commands are applied.

    Currently, the following 7 scopes are supported:

    - :obj:`~pyFipper.types.BotCommandScopeDefault`
    - :obj:`~pyFipper.types.BotCommandScopeAllPrivateChats`
    - :obj:`~pyFipper.types.BotCommandScopeAllGroupChats`
    - :obj:`~pyFipper.types.BotCommandScopeAllChatAdministrators`
    - :obj:`~pyFipper.types.BotCommandScopeChat`
    - :obj:`~pyFipper.types.BotCommandScopeChatAdministrators`
    - :obj:`~pyFipper.types.BotCommandScopeChatMember`

    **Determining list of commands**

    The following algorithm is used to determine the list of commands for a particular user viewing the bot menu.
    The first list of commands which is set is returned:

    **Commands in the chat with the bot**:

    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllPrivateChats + language_code
    - BotCommandScopeAllPrivateChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault

    **Commands in group and supergroup chats**

    - BotCommandScopeChatMember + language_code
    - BotCommandScopeChatMember
    - BotCommandScopeChatAdministrators + language_code (administrators only)
    - BotCommandScopeChatAdministrators (administrators only)
    - BotCommandScopeChat + language_code
    - BotCommandScopeChat
    - BotCommandScopeAllChatAdministrators + language_code (administrators only)
    - BotCommandScopeAllChatAdministrators (administrators only)
    - BotCommandScopeAllGroupChats + language_code
    - BotCommandScopeAllGroupChats
    - BotCommandScopeDefault + language_code
    - BotCommandScopeDefault
    """

    def __init__(self, type: str):
        super().__init__()
        self.type = type

    async def write(self, client: 'pyFipper.Client') -> 'raw.base.BotCommandScope':
        raise NotImplementedError