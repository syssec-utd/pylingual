import boto3
import re
from cli.config import config
import os
from .common import Source, SourcedItem

class S3Source(Source):
    URI_re = re.compile('^s3://(?P<bucket_name>[a-zA-Z0-9.\\-_]{1,255})/(?P<prefix>.*)$')

    def get_client(self):
        return boto3.client('s3', aws_access_key_id=os.getenv('AWS_SERVER_PUBLIC_KEY'), aws_secret_access_key=os.getenv('AWS_SERVER_SECRET_KEY'), region_name=config.S3_REGION, config=boto3.session.Config(signature_version='s3v4', s3={'addressing_style': 'path'}))

    def list_contents(self, starts_with='', ends_with=''):
        match = self.URI_re.match(self.uri)
        terms = match.groupdict()
        client = self.get_client()
        prefix = terms.get('prefix', '') + starts_with
        paginator = client.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=terms.get('bucket_name'), Prefix=prefix)
        if len(ends_with) > 0:
            search = f'Contents[?ends_with(Key, `{ends_with}`)][]'
            for item in page_iterator.search(search):
                yield SourcedItem(item, item['Key'], self)
            return
        for page in page_iterator:
            for item in page['Contents']:
                yield SourcedItem(item, item['Key'], self)

    def open(self, reference):
        client = self.get_client()
        reference_path = reference.get('Key')
        reference_response = client.get_object(Bucket='client-research-data', Key=reference_path)
        file_size = reference_response['ContentLength']
        stream = reference_response['Body']
        modified = reference_response['LastModified']
        return (reference_path, file_size, modified, stream)