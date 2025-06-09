import sys
import argparse
import getpass
import nwebclient as n
from usersettings import Settings
parser = argparse.ArgumentParser()
parser.add_argument('-v', help='increase output verbosity', action='store_const', const=True)
parser.add_argument('-s', type=int, help='display a square of a given number')
parser.add_argument('-param1', help='echo the string you use here', default='')
parser.add_argument('op', help='Operation (setup)')
args = parser.parse_args()
CONF = Settings('nweb')
CONF.add_setting('nweburl', str, default='')
CONF.load_settings()

def help():
    print('Python Cli App')
    print('')
    print('Call: python -m nwebclient operation')
    print('')
    print(' operation: setup, i, help')

def setup():
    print('Execute Setup')
    import os
    os.system('curl https://bsnx.net/d/nweb-install.sh | /bin/bash')

def i_help():
    print('')
    print('NWeb Commands')
    print('')
    print(' 1) view docs')
    print(' 2) download image')
    print('')
    print(' exit')
    print('')

def i_docs(client):
    try:
        docs = client.docs()
        for d in docs:
            print(d.title())
    except ValueError:
        print('Invalid JSON-Response, maybe wrong password or server-error')

def i_download_images(client):
    client.downloadImages()

def interactive():
    print('nweb-url e.g. https://host/4.0/ ')
    print('Enter nweb-URL[' + CONF.nweburl + ']: ')
    url = sys.stdin.readline().strip()
    print('Enter Username:')
    user = sys.stdin.readline().strip()
    print('Enter Password:')
    pw = getpass.getpass(prompt='Password: ', stream=None)
    if url == '':
        url = CONF.nweburl
    else:
        CONF.nweburl = url
    CONF.save_settings()
    print('URL: ' + url)
    print('User: ' + user)
    print('Password: ***')
    client = n.NWebClient(url, user, pw)
    cmd = ''
    while cmd != 'exit':
        i_help()
        if cmd == '1':
            i_docs(client)
        elif cmd == '2':
            i_download_images(client)
        cmd = sys.stdin.readline().strip()
if args.v:
    print('verbosity turned on')
print('+----------------------+')
print('| nweb client main     |')
print('+----------------------+')
if args.op == 'setup':
    setup()
elif args.op == 'i':
    interactive()
elif args.op == 'help':
    help()
else:
    print('Unknown Operation')
    print('OP:' + args.op)
    print(args.param1)