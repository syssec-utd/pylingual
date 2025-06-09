async def delete_conversation_member(self, context: TurnContext, member_id: str) -> None:
    """
        Deletes a member from the current conversation.
        :param context:
        :param member_id:
        :return:
        """
    try:
        if not context.activity.service_url:
            raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing service_url')
        if not context.activity.conversation or not context.activity.conversation.id:
            raise TypeError('BotFrameworkAdapter.delete_conversation_member(): missing conversation or conversation.id')
        service_url = context.activity.service_url
        conversation_id = context.activity.conversation.id
        client = self.create_connector_client(service_url)
        return await client.conversations.delete_conversation_member(conversation_id, member_id)
    except AttributeError as attr_e:
        raise attr_e
    except Exception as e:
        raise e