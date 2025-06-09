from .colors import Colors
from .exceptions import LoginError
import datetime
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET

class Costume:

    def __init__(self, character, id, name, ordinal=None, colors=None, lastPortrait=0, lastScale=100, lastGloam=0, lastSpecitag=0, standard=200, desc=''):
        self.character = character
        self.id = id
        self.name = name
        self.ordinal = ordinal
        self.colors = colors
        self.lastPortrait = lastPortrait
        self.lastScale = lastScale
        self.lastGloam = lastGloam
        self.lastSpecitag = lastSpecitag
        self.standard = standard
        self.desc = desc

class Character:
    TYPE_INI = 0
    TYPE_ACCOUNT = 1

    def __init__(self):
        self.name = ''
        self.id = 0
        self.account = None
        self.colors = None
        self.password = None
        self.desc = None
        self.logins = 0
        self.lastLogin = 0
        self.autoResponse = None
        self.autoResponseMessage = None
        self.AFKTime = None
        self.AFKMessage = None
        self.AFKDescription = None
        self.AFKPortrait = None
        self.DefaultPortrait = None
        self.AFKDisconnectTime = None
        self.species = None
        self.flags = None
        self.lastItem = None
        self.lastPort = None
        self.lastScale = None
        self.lastGloam = None
        self.lastSpeci = None
        self.messages = None
        self.time = None
        self.owner = None
        self.costumes = None
        self.type = self.TYPE_INI

    @classmethod
    def fromINI(self, name, colors=None, password=None, desc=None, logins=0, lastLogin=0, autoResponse=None, autoResponseMessage=None, AFKTime=None, AFKMessage=None, AFKDescription=None, AFKPortrait=None, DefaultPortrait=None, AFKDisconnectTime=None):
        self = cls()
        self.type = self.TYPE_INI
        return self

    @classmethod
    def fromAccount(cls, account, id, name, species=None, colors=None, flags=None, created=None, lastLogin=None, lastItem=None, lastPort=None, lastScale=100, lastGloam=None, lastSpeci=None, messages=None, logins=0, time=None, owner=None, desc=None, costumes=None):
        self = cls()
        self.type = self.TYPE_ACCOUNT
        self.account = account
        self.id = id
        self.name = name
        self.species = species
        self.colors = colors
        self.flags = flags
        self.created = created
        self.lastLogin = lastLogin
        self.lastItem = lastItem
        self.lastPort = lastPort
        self.lastScale = lastScale
        self.lastGloam = lastGloam
        self.lastSpeci = lastSpeci
        self.messages = messages
        self.logins = logins
        self.time = time
        self.owner = owner
        self.desc = desc
        self.costumes = costumes or []
        return self

    def addCostume(self, costume):
        if self.costumes:
            self.costumes.append(costume)

class Account:
    loginServer = 'https://charon.furcadia.com/accounts/clogin.php'

    def __init__(self, username, password, id, email=None):
        self.username = username
        self.password = password
        self.id = id
        self.email = email
        self.characters = []
        pass

    def addCharacter(self, char):
        self.characters.append(char)

    def findCharacter(self, charname):
        for character in self.characters:
            if character.name.lower() == charname.lower():
                return character
        return None

    @classmethod
    def login(cls, username, password, loginServer=None):
        data = urllib.parse.urlencode({'u': username, 'p': password, 'k': 'ZAWJuuaTpRrG-Furcadia-KFzsVWwpPM9t', 'v': 'libfurc'})
        req = urllib.request.Request(loginServer or cls.loginServer, data=data.encode(), headers={'Content-Type': 'application/x-www-form-urlencoded'}, method='POST')
        try:
            with urllib.request.urlopen(req) as res:
                root = ET.fromstring(res.read())
                account = None
                for child in root:
                    if child.tag == 'account':
                        account = child
                        break
                if account == None:
                    raise exceptions.LoginError('No account element located!')
                self = cls(username, password, int(account.attrib['id']), account.attrib.get('email', None))
                for character in account:
                    char = Character.fromAccount(self, id=character.attrib['id'], name=character.attrib['name'], species=character.attrib['species'], colors=Colors.fromCode(character.attrib['colors']), flags=int(character.attrib['flags']), created=datetime.datetime.strptime(character.attrib['created'], '%Y-%m-%d %H:%M:%S'), lastLogin=datetime.datetime.strptime(character.attrib['lastlogin'], '%Y-%m-%d %H:%M:%S'), lastItem=int(character.attrib['lastitem']), lastPort=int(character.attrib['lastport']), lastScale=int(character.attrib['lastscale']), lastGloam=int(character.attrib['lastgloam']), lastSpeci=int(character.attrib['lastspeci']), messages=int(character.attrib['messages']), logins=int(character.attrib['logins']), time=int(character.attrib['time']), owner=character.attrib['owner'])
                    for costume in character:
                        if costume.tag == 'costume':
                            char.addCostume(Costume(character=char, id=int(costume.attrib['id']), name=costume.attrib['name'], ordinal=int(costume.attrib['ordinal']), colors=Colors.fromCode(costume.attrib['colors']), lastPortrait=int(costume.attrib['last_portrait']), lastScale=int(costume.attrib['last_scale']), lastGloam=int(costume.attrib['last_gloam']), lastSpecitag=int(costume.attrib['last_specitag']), standard=int(costume.attrib['standard']), desc=costume.text))
                        elif costume.tag == 'desc':
                            char.desc = costume.text
                    self.addCharacter(char)
        except urllib.error.HTTPError as e:
            raise exceptions.LoginError(e.read()) from None
        return self