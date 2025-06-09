from typing import Union
import pyFipper
from pyFipper import raw

class UnpinAllChatMessages:

    async def unpin_all_chat_messages(self: 'pyFipper.Client', chat_id: Union[int, str]) -> bool:
        """Use this method to clear the list of pinned messages in a chat.
        If the chat is not a private chat, the bot must be an administrator in the chat for this to work and must have
        the 'can_pin_messages' admin right in a supergroup or 'can_edit_messages' admin right in a channel.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Unpin all chat messages
                await app.unpin_all_chat_messages(chat_id)
        """
        await self.invoke(raw.functions.messages.UnpinAllMessages(peer=await self.resolve_peer(chat_id)))
        return True