def _del_conversation(self, conversation_key: str) -> None:
    """Deletes Conversation instance.

        Args:
            conversation_key: Conversation key.
        """
    if conversation_key in self.conversations.keys():
        del self.conversations[conversation_key]
        log.info(f'Deleted conversation, key: {conversation_key}')