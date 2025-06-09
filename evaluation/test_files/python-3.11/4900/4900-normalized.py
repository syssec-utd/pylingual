def __get_award_emoji(self, item_type, item_id):
    """Get award emojis for issue/merge request"""
    emojis = []
    group_emojis = self.client.emojis(item_type, item_id)
    for raw_emojis in group_emojis:
        for emoji in json.loads(raw_emojis):
            emojis.append(emoji)
    return emojis