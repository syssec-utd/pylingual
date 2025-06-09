def get_chat_id(self, username):
    """Lookup chat_id of username if chat_id is unknown via API call."""
    if username is not None:
        chats = requests.get(self.base_url + '/getUpdates').json()
        user = username.split('@')[-1]
        for chat in chats['result']:
            if chat['message']['from']['username'] == user:
                return chat['message']['from']['id']