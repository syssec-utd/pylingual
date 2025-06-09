import os
import requests
import hashlib
from . import acquisition
from urllib.parse import urlparse
from urllib.parse import parse_qsl

class AcquisitionURL(acquisition.Acquisition):

    def __init__(self, name, orchestrator_ref, settings):
        super().__init__(name=name, orchestrator_ref=orchestrator_ref, settings=settings, channel='url')

    def new_files(self, dls, last_hash):
        urls = dls['acquisition']['channel']['url']
        if type(urls) == str:
            urls = [urls]
        hashes = last_hash.split('|')
        pairs = [(urls[i], hashes[i] if i < len(hashes) else '') for i in range(0, len(urls))]
        source_dir = self.source_path(dls)
        current_hash = []
        files_to_pipeline = []
        for url, last_hash in pairs:
            parts = urlparse(url)
            if 'file_name' not in dls['acquisition']['channel']:
                dest_name = parts.path.replace('/', '_')
            elif type(dls['acquisition']['channel']['file_name']) == str:
                dest_name = dls['acquisition']['channel']['file_name']
            else:
                dest_name = ''
                for p in dls['acquisition']['channel']['file_name']:
                    if p.startswith('query.'):
                        for par, val in parse_qsl(parts.query):
                            if p == f'query.{par}':
                                dest_name = f'{dest_name}_{par}-{val}'
                    elif p == 'netloc':
                        dest_name = f"{dest_name}_{parts.netloc.replace('/', '_')}"
                    elif p == 'path':
                        dest_name = f"{dest_name}_{parts.path.replace('/', '_')}"
                if dest_name == '':
                    dest_name = parts.path.replace('/', '_')
            file_path = self.source_path(dls, dest_name)
            r = requests.get(url)
            current_hash.append(r.headers.get('ETag') if r.headers.get('Etag') is not None else hashlib.sha1(r.content).hexdigest())
            if not os.path.exists(file_path) or last_hash == '':
                with open(file_path, 'wb') as cont:
                    cont.write(r.content)
                files_to_pipeline.extend([file_path])
            elif current_hash[-1] != last_hash:
                with open(file_path, 'wb') as cont:
                    cont.write(r.content)
                files_to_pipeline.extend([file_path])
        return {'hash': '|'.join(current_hash), 'files': files_to_pipeline}