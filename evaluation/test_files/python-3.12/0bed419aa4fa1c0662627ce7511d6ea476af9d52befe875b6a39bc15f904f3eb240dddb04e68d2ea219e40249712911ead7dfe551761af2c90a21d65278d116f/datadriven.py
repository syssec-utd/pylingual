import os
import time
import json
import requests
import threading
from . import package

class Token:

    def __init__(self):
        self._ip = os.getenv('APPMAN_HOST_IP', default='localhost')
        self._port = os.getenv('APPMAN_HOST_PORT', default=59000)
        self._prefix = os.getenv('MX_API_VER', default='api/v1/')
        with open('/var/run/mx-api-token') as f:
            token = f.readline()
            self._headers = {'Content-Type': 'application/json', 'mx-api-token': token.strip()}

class Listener(Token):

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.__config = package.Configuration()
        self.__tag_url = 'http://{}:{}/{}tags/monitor'.format(self._ip, self._port, self._prefix)
        self.__event_url = 'http://{}:{}/{}events'.format(self._ip, self._port, self._prefix)

    def __get_tag_endpoint(self):
        urls = []
        tag_list = self.__config.data_driven_tags()
        for provider, sources in tag_list.items():
            for source, tags in sources.items():
                sep = ','
                url = '{}/{}/{}?tags={}&onChanged'.format(self.__tag_url, provider, source, sep.join(tags))
                urls.append(url)
        return urls

    def __get_event_endpoint(self):
        sep = ','
        names = []
        categories = []
        event_list = self.__config.data_driven_events()
        for category, ns in event_list.items():
            categories.append(category)
            names = names + ns
        if not (len(categories) and len(names)):
            return ''
        return '{}?categories={}&eventNames={}&event=true'.format(self.__event_url, sep.join(categories), sep.join(names))

    def __start_monitoring(self, _type, url):
        while True:
            try:
                r = requests.get(url, headers=self._headers, stream=True)
                if r.encoding is None:
                    r.encoding = 'utf-8'
                for line in r.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            if hasattr(self, 'callback') and 'data:' in line:
                                self.callback(_type=_type, data=json.loads(line[5:]))
                        except Exception as err:
                            print('Err: {}, {}'.format(err, line))
            except Exception as e:
                print(e)
            time.sleep(1)

    def listen(self):
        urls = {}
        for tag_url in self.__get_tag_endpoint():
            urls[tag_url] = 'tag'
        evt_url = self.__get_event_endpoint()
        if evt_url != '':
            urls[evt_url] = 'event'
        for url, _type in urls.items():
            threading.Thread(target=self.__start_monitoring, args=(_type, url), daemon=True).start()