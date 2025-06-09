import requests
from docarray import Document
from deployment.bff.app.v1.routers.helper import jina_client_post
API_KEY = 'my_key'
url = f'https://nowrun.jina.ai/api/v1/search-app/search'
host = 'grpcs://nowapi-c74eae8ebe.wolf.jina.ai'
url = 'http://localhost:8080/api/v1/search-app/search'
host = 'grpc://0.0.0.0'
port = 9090
direct = False
if direct:
    result = jina_client_post(host, -1, '/search', Document(chunks=Document(text='girl on motorbike')), {'api_key': API_KEY})
    for match in result[0].matches:
        print(match.tags['uri'])
else:
    request_body = {'host': host, 'port': port, 'api_key': API_KEY, 'fields': {'index_field_name': {'text': 'girl on motorbike'}}}
    response = requests.post(url, json=request_body)
if 'message' in response.json():
    print(response.json()['message'])