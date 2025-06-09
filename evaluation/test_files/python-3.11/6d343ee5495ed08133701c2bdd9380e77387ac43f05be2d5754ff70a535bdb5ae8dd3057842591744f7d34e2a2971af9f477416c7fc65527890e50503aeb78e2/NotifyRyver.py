import re
import requests
from json import dumps
from .NotifyBase import NotifyBase
from ..common import NotifyImageSize
from ..common import NotifyType
from ..utils import parse_bool
from ..utils import validate_regex
from ..AppriseLocale import gettext_lazy as _

class RyverWebhookMode:
    """
    Ryver supports to webhook modes
    """
    SLACK = 'slack'
    RYVER = 'ryver'
RYVER_WEBHOOK_MODES = (RyverWebhookMode.SLACK, RyverWebhookMode.RYVER)

class NotifyRyver(NotifyBase):
    """
    A wrapper for Ryver Notifications
    """
    service_name = 'Ryver'
    service_url = 'https://ryver.com/'
    secure_protocol = 'ryver'
    setup_url = 'https://github.com/caronc/apprise/wiki/Notify_ryver'
    image_size = NotifyImageSize.XY_72
    body_maxlen = 1000
    templates = ('{schema}://{organization}/{token}', '{schema}://{user}@{organization}/{token}')
    template_tokens = dict(NotifyBase.template_tokens, **{'organization': {'name': _('Organization'), 'type': 'string', 'required': True, 'regex': ('^[A-Z0-9_-]{3,32}$', 'i')}, 'token': {'name': _('Token'), 'type': 'string', 'required': True, 'private': True, 'regex': ('^[A-Z0-9]{15}$', 'i')}, 'user': {'name': _('Bot Name'), 'type': 'string'}})
    template_args = dict(NotifyBase.template_args, **{'mode': {'name': _('Webhook Mode'), 'type': 'choice:string', 'values': RYVER_WEBHOOK_MODES, 'default': RyverWebhookMode.RYVER}, 'image': {'name': _('Include Image'), 'type': 'bool', 'default': True, 'map_to': 'include_image'}})

    def __init__(self, organization, token, mode=RyverWebhookMode.RYVER, include_image=True, **kwargs):
        """
        Initialize Ryver Object
        """
        super().__init__(**kwargs)
        self.token = validate_regex(token, *self.template_tokens['token']['regex'])
        if not self.token:
            msg = 'An invalid Ryver API Token ({}) was specified.'.format(token)
            self.logger.warning(msg)
            raise TypeError(msg)
        self.organization = validate_regex(organization, *self.template_tokens['organization']['regex'])
        if not self.organization:
            msg = 'An invalid Ryver Organization ({}) was specified.'.format(organization)
            self.logger.warning(msg)
            raise TypeError(msg)
        self.mode = None if not isinstance(mode, str) else mode.lower()
        if self.mode not in RYVER_WEBHOOK_MODES:
            msg = 'The Ryver webhook mode specified ({}) is invalid.'.format(mode)
            self.logger.warning(msg)
            raise TypeError(msg)
        self.include_image = include_image
        self._re_formatting_map = {'\\r\\*\\n': '\\n', '&': '&amp;', '<': '&lt;', '>': '&gt;'}
        self._re_formatting_rules = re.compile('(' + '|'.join(self._re_formatting_map.keys()) + ')', re.IGNORECASE)
        return

    def send(self, body, title='', notify_type=NotifyType.INFO, **kwargs):
        """
        Perform Ryver Notification
        """
        headers = {'User-Agent': self.app_id, 'Content-Type': 'application/json'}
        if self.mode == RyverWebhookMode.SLACK:
            title = self._re_formatting_rules.sub(lambda x: self._re_formatting_map[x.group()], title)
            body = self._re_formatting_rules.sub(lambda x: self._re_formatting_map[x.group()], body)
        url = 'https://{}.ryver.com/application/webhook/{}'.format(self.organization, self.token)
        payload = {'body': body if not title else '**{}**\r\n{}'.format(title, body), 'createSource': {'displayName': self.user, 'avatar': None}}
        image_url = None if not self.include_image else self.image_url(notify_type)
        if image_url:
            payload['createSource']['avatar'] = image_url
        self.logger.debug('Ryver POST URL: %s (cert_verify=%r)' % (url, self.verify_certificate))
        self.logger.debug('Ryver Payload: %s' % str(payload))
        self.throttle()
        try:
            r = requests.post(url, data=dumps(payload), headers=headers, verify=self.verify_certificate, timeout=self.request_timeout)
            if r.status_code != requests.codes.ok:
                status_str = NotifyBase.http_response_code_lookup(r.status_code)
                self.logger.warning('Failed to send Ryver notification: {}{}error={}.'.format(status_str, ', ' if status_str else '', r.status_code))
                self.logger.debug('Response Details:\r\n{}'.format(r.content))
                return False
            else:
                self.logger.info('Sent Ryver notification.')
        except requests.RequestException as e:
            self.logger.warning('A Connection error occurred sending Ryver:%s ' % self.organization + 'notification.')
            self.logger.debug('Socket Exception: %s' % str(e))
            return False
        return True

    def url(self, privacy=False, *args, **kwargs):
        """
        Returns the URL built dynamically based on specified arguments.
        """
        params = {'image': 'yes' if self.include_image else 'no', 'mode': self.mode}
        params.update(self.url_parameters(*args, privacy=privacy, **kwargs))
        botname = ''
        if self.user:
            botname = '{botname}@'.format(botname=NotifyRyver.quote(self.user, safe=''))
        return '{schema}://{botname}{organization}/{token}/?{params}'.format(schema=self.secure_protocol, botname=botname, organization=NotifyRyver.quote(self.organization, safe=''), token=self.pprint(self.token, privacy, safe=''), params=NotifyRyver.urlencode(params))

    @staticmethod
    def parse_url(url):
        """
        Parses the URL and returns enough arguments that can allow
        us to re-instantiate this object.

        """
        results = NotifyBase.parse_url(url, verify_host=False)
        if not results:
            return results
        results['organization'] = NotifyRyver.unquote(results['host'])
        try:
            results['token'] = NotifyRyver.split_path(results['fullpath'])[0]
        except IndexError:
            results['token'] = None
        results['mode'] = results['qsd'].get('mode', RyverWebhookMode.RYVER)
        results['include_image'] = parse_bool(results['qsd'].get('image', True))
        return results

    @staticmethod
    def parse_native_url(url):
        """
        Support https://RYVER_ORG.ryver.com/application/webhook/TOKEN
        """
        result = re.match('^https?://(?P<org>[A-Z0-9_-]+)\\.ryver\\.com/application/webhook/(?P<webhook_token>[A-Z0-9]+)/?(?P<params>\\?.+)?$', url, re.I)
        if result:
            return NotifyRyver.parse_url('{schema}://{org}/{webhook_token}/{params}'.format(schema=NotifyRyver.secure_protocol, org=result.group('org'), webhook_token=result.group('webhook_token'), params='' if not result.group('params') else result.group('params')))
        return None