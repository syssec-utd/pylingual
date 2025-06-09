import requests
import json
import os
import sys
import tempfile
from os.path import expanduser
HOME = expanduser('~')
TMP_DIR = tempfile.gettempdir()
conf_path = '.cookie_cloud.json'
if not os.path.isfile(conf_path):
    conf_path = os.path.join(HOME, '.cookie_cloud.json')
COOKIES_PATH = os.path.join(TMP_DIR, 'cookies.json')
conf = json.load(open(conf_path)) if os.path.isfile(conf_path) else {}
headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'token ' + conf['github_token']}

def git_get(url):
    return json.loads(requests.get(url, headers=headers).content)

def get_comment_body(issue_url):
    data = {}
    if issue_url:
        data = git_get('{}/comments?per_page=100'.format(issue_url))
    if not data:
        return data
    try:
        return json.loads(data[-1]['body'])
    except:
        return data[-1]['body']

def get_issue_url(site):
    url = 'https://api.github.com/repos/' + conf['github_user'] + '/' + conf['github_repo'] + '/issues?labels=' + site
    data = git_get(url)
    if not data:
        return
    return data[-1]['url']

def get_cookie(site, update=False, raw=False, user=None, repo=None):
    global conf
    cookies = {}
    if user and repo:
        conf['github_user'] = user
        conf['github_repo'] = repo
    if os.path.isfile(COOKIES_PATH) and (not update):
        cookies_str = open(COOKIES_PATH).read()
        cookies = json.loads(cookies_str) if cookies_str else {}
    if cookies.get(site):
        return cookies[site]
    data = get_comment_body(get_issue_url(site))
    cookie = data
    if isinstance(data, dict) and (not raw):
        for i in data:
            cookie += i['name'] + '=' + i['value'] + ';'
    save_cookie(site, cookie)
    return cookie

def save_cookie(site, cookie_str):
    cookies = {}
    if os.path.isfile(COOKIES_PATH):
        cookies_str = open(COOKIES_PATH).read()
        cookies = json.loads(cookies_str) if cookies_str else {}
    cookies[site] = cookie_str
    open(COOKIES_PATH, 'w').write(json.dumps(cookies, indent=4))