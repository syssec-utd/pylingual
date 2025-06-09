"""
All the operators related to communication are here.
"""
from nbox import Operator

class Notify(Operator):
    _mode_to_packages = {'slack': 'slackclient', 'ms_teams': 'microsoft-teams', 'discord': 'discord'}

    def __init__(self, slack_connect: str=None, ms_teams: str=None, discord: str=None):
        """Notifications"""
        super().__init__()
        self.notify_mode = None
        self.notify_id = None
        for mode, id in [('slack', slack_connect), ('ms_teams', ms_teams), ('discord', discord)]:
            if id:
                self.notify_mode = mode
                self.notify_id = id
                import importlib
                try:
                    importlib.import_module(self._mode_to_packages[mode])
                except ImportError:
                    raise Exception(f'{self._mode_to_packages[mode]} package required for {mode}')
                break
        if not self.notify_mode:
            raise Exception('No notification mode specified')

    def forward(self, message: str, **kwargs):
        package = self._mode_to_packages[self.notify_mode]
        import importlib
        importlib.import_module(package)
        if self.notify_mode == 'slack':
            from slackclient import SlackClient
            sc = SlackClient(self.notify_id)
            sc.api_call('chat.postMessage', text=message, **kwargs)
        elif self.notify_mode == 'ms_teams':
            from microsoft_teams.api_client import TeamsApiClient
            from microsoft_teams.models import MessageCard
            client = TeamsApiClient(self.notify_id)
            client.connect()
            client.send_message(MessageCard(text=message, **kwargs))
        elif self.notify_mode == 'discord':
            from discord import Webhook, RequestsWebhookAdapter
            webhook = Webhook.from_url(self.notify_id, adapter=RequestsWebhookAdapter())
            webhook.send(message, **kwargs)