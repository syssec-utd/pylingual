""" ASF LDAP Account Manager """
import sys
assert sys.version_info >= (3, 2)
import ldap
import ldap.modlist
import ldif
import re
import crypt
import random
import string
LDAP_SANDBOX = 'ldaps://ldap-sandbox.apache.org:636'
LDAP_MASTER = 'ldaps://ldap-master.apache.org:636'
LDAP_SUFFIX = 'dc=apache,dc=org'
LDAP_PEOPLE_BASE = 'ou=people,dc=apache,dc=org'
LDAP_GROUPS_BASE = 'ou=groups,dc=apache,dc=org'
LDAP_APLDAP_BASE = 'cn=apldap,ou=groups,ou=services,dc=apache,dc=org'
LDAP_CHAIRS_BASE = 'cn=pmc-chairs,ou=groups,ou=services,dc=apache,dc=org'
LDAP_PMCS_BASE = 'ou=project,ou=groups,dc=apache,dc=org'
LDAP_ROLES_BASE = 'ou=role,ou=groups,dc=apache,dc=org'
LDAP_DN = 'uid=%s,ou=people,dc=apache,dc=org'
LDAP_CN = 'cn=%s,%s'
LDAP_VALID_UID_RE = re.compile('^[a-z0-9][a-z0-9_]+$')
MINIMUM_USER_UID = 6000
MINIMUM_SVC_UID = 5010
assert MINIMUM_USER_UID > MINIMUM_SVC_UID
ASSERTION_FAILED = 'Common backend assertions failed, LDAP corruption?'
BACKEND_TIMEOUT = 'The backend authentication server timed out, please retry later.'

def bytify(ldiff):
    """ Convert all values in a dict to byte-string """
    for (k, v) in ldiff.items():
        if type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is str:
                    v[n] = xv.encode('utf-8')
                n += 1
        elif type(v) is str:
            v = [v.encode('utf-8')]
        ldiff[k] = v
    return ldiff

def stringify(ldiff):
    """ Convert all values in a dict to string """
    for (k, v) in ldiff.items():
        if type(v) is list and len(v) == 1:
            v = v[0]
        if type(v) is list:
            n = 0
            for xv in v:
                if type(v[n]) is bytes:
                    v[n] = xv.decode('utf-8')
                n += 1
        elif type(v) is bytes:
            v = v.decode('utf-8')
        ldiff[k] = v
    return ldiff

class ConnectionException(Exception):
    """ Simple exception with a message and an optional origin exception (WIP) """

    def __init__(self, message, origin=None):
        super().__init__(message)
        self.origin = origin

class ValidatorException(Exception):
    """ Simple validator exception with a message and an optional triggering attribute """

    def __init__(self, message, attrib=None):
        super().__init__(message)
        self.attribute = attrib

class committer:
    """ Committer class, allows for munging data """

    def __init__(self, mgr, res):
        self.manager = mgr
        self.dn = res[0][0]
        self.dn_enc = self.dn.encode('ascii')
        self.attributes = stringify(res[0][1])
        self.uid = self.attributes['uid']

    def add_project(self, project):
        """ Add person to project (as committer) """
        dn = LDAP_CN % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'member', self.dn_enc)])

    def add_pmc(self, project):
        """ Add person to project (as PMC member) """
        dn = LDAP_CN % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'owner', self.dn_enc)])

    def add_basic_group(self, group):
        """ Add person to basic posixGroup entry """
        dn = LDAP_CN % (group, LDAP_GROUPS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'memberUid', self.uid.encode('ascii'))])

    def add_role(self, role):
        """ Add person to basic posixGroup entry """
        dn = LDAP_CN % (role, LDAP_ROLES_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_ADD, 'member', self.dn_enc)])

    def remove_project(self, project):
        """ Remove person from project (as committer) """
        dn = LDAP_CN % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'member', self.dn_enc)])

    def remove_pmc(self, project):
        """ Remove person from PMC """
        dn = LDAP_CN % (project, LDAP_PMCS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'owner', self.dn_enc)])

    def remove_basic_group(self, group):
        """ Remove person from basic posixGroup entry """
        dn = LDAP_CN % (group, LDAP_GROUPS_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'memberUid', self.uid.encode('ascii'))])

    def remove_role(self, role):
        """ Add person to basic posixGroup entry """
        dn = LDAP_CN % (role, LDAP_ROLES_BASE)
        self.manager.lc.modify_s(dn, [(ldap.MOD_DELETE, 'member', self.dn_enc)])

    def rename(self, newuid):
        """ Rename an account, fixing in all projects """
        xuid = newuid
        if type(newuid) is str:
            newuid = newuid.encode('ascii')
        else:
            xuid = newuid.decode('ascii')
        if not LDAP_VALID_UID_RE.match(xuid):
            raise ValidatorException('Invalid UID, must match ^[a-z0-9][a-z0-9_]+$')
        if self.manager.load_account(xuid):
            raise ConnectionException('An account with this uid already exists')
        res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, 'cn=%s' % xuid)
        if res:
            raise ValidatorException('availid clashes with project name %s!' % res[0][0], 'uid')
        uidnumber = self.manager.next_user_uid()
        changeset = []
        o_email = self.attributes['asf-committer-email'].encode('ascii')
        n_email = b'%s@apache.org' % newuid
        o_homedir = self.attributes['homeDirectory'].encode('ascii')
        n_homedir = b'/home/%s' % newuid
        changeset.append((ldap.MOD_DELETE, 'asf-committer-email', o_email))
        changeset.append((ldap.MOD_ADD, 'asf-committer-email', n_email))
        changeset.append((ldap.MOD_DELETE, 'homeDirectory', o_homedir))
        changeset.append((ldap.MOD_ADD, 'homeDirectory', n_homedir))
        ouidn = self.attributes['uidNumber'].encode('ascii')
        nuidn = b'%u' % uidnumber
        print('Changing uidNumber/gidNumber to %s...' % uidnumber)
        changeset.append((ldap.MOD_DELETE, 'gidNumber', ouidn))
        changeset.append((ldap.MOD_ADD, 'gidNumber', nuidn))
        changeset.append((ldap.MOD_DELETE, 'uidNumber', ouidn))
        changeset.append((ldap.MOD_ADD, 'uidNumber', nuidn))
        self.manager.lc.modify_s(self.dn, changeset)
        odn = self.dn_enc.decode('ascii')
        newdn = LDAP_DN % xuid
        newdn_enc = newdn.encode('ascii')
        print('Changing %s to %s' % (odn, newdn))
        self.manager.lc.modrdn_s(odn, 'uid=%s' % xuid)
        for role in ['member', 'owner']:
            res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, '%s=%s' % (role, self.dn_enc.decode('ascii')))
            for entry in res:
                cn = entry[0]
                myhash = entry[1]
                if self.dn_enc in myhash[role]:
                    print('Modifying (long) %s attribute in %s ...' % (role, cn))
                    self.manager.lc.modify_s(cn, [(ldap.MOD_DELETE, role, self.dn_enc)])
                    self.manager.lc.modify_s(cn, [(ldap.MOD_ADD, role, newdn_enc)])
        ouid = self.uid.encode('ascii')
        for role in ['memberUid']:
            res = self.manager.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, '(&(objectClass=posixGroup)(%s=%s))' % (role, self.uid))
            for entry in res:
                cn = entry[0]
                myhash = entry[1]
                if ouid in myhash[role]:
                    print('Modifying (short) %s attribute in %s ...' % (role, cn))
                    self.manager.lc.modify_s(cn, [(ldap.MOD_DELETE, role, ouid)])
                    self.manager.lc.modify_s(cn, [(ldap.MOD_ADD, role, newuid)])
        self.uid = xuid
        self.dn_enc = newdn_enc

class manager:
    """ Top LDAP Manager class for whomever is using the script """

    def __init__(self, user, password, host=LDAP_SANDBOX):
        if not re.match('^[-_a-z0-9]+$', user):
            raise ConnectionException('Invalid characters in User ID. Must be alphanumerical or dashes only.')
        lc = ldap.initialize(host)
        lc.set_option(ldap.OPT_REFERRALS, 0)
        lc.set_option(ldap.OPT_TIMEOUT, 5)
        try:
            lc.simple_bind_s(LDAP_DN % user, password)
        except ldap.INVALID_CREDENTIALS:
            raise ConnectionException('Invalid username or password supplied!')
        except ldap.TIMEOUT:
            raise ConnectionException(BACKEND_TIMEOUT)
        self.uid = user
        self.dn = LDAP_DN % user
        self.lc = lc
        try:
            res = lc.search_s(LDAP_DN % user, ldap.SCOPE_BASE)
            assert len(res) == 1
            assert len(res[0]) == 2
            fn = res[0][1].get('cn')
            assert type(fn) is list and len(fn) == 1
            self.fullname = str(fn[0], 'utf-8')
            self.email = '%s@apache.org' % user
        except ldap.TIMEOUT:
            raise ConnectionException(BACKEND_TIMEOUT)
        except AssertionError:
            raise ConnectionException(ASSERTION_FAILED)
        try:
            res = lc.search_s(LDAP_APLDAP_BASE, ldap.SCOPE_BASE)
            assert len(res) == 1
            assert len(res[0]) == 2
            members = res[0][1].get('member')
            assert type(members) is list and len(members) > 0
            self.isAdmin = bytes(LDAP_DN % user, 'utf-8') in members
        except ldap.TIMEOUT:
            raise ConnectionException(BACKEND_TIMEOUT)
        except AssertionError:
            raise ConnectionException(ASSERTION_FAILED)

    def load_account(self, uid):
        if type(uid) is bytes:
            uid = uid.decode('ascii')
        res = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uid=%s' % uid)
        if res:
            return committer(self, res)
        return None

    def _find_gaps(self, l):
        return [item for item in range(l[0], l[-1] + 1) if item not in l]

    def next_user_uid(self):
        """ Find lowest available user account uid with a matching available gid """
        try:
            r = self.lc.search_s(LDAP_PEOPLE_BASE, ldap.SCOPE_SUBTREE, 'uid=*', ['uidNumber', 'gidNumber'])
            un_avail_uids = sorted([int(item[1]['uidNumber'][0].decode('utf8')) for item in r])
            un_avail_gids = sorted([int(item[1]['gidNumber'][0].decode('utf8')) for item in r])
            avail_uids = self._find_gaps(un_avail_uids)
            avail_gids = self._find_gaps(un_avail_gids)
            n_uid = int(un_avail_uids[-1] + 1)
            while n_uid in un_avail_gids:
                n_uid += 1
            avail_uids.append(n_uid)
            assert type(avail_uids) is list and len(avail_uids) > 0 and (type(avail_gids) is list) and (len(avail_gids) > 0)
            for uid in avail_uids:
                if uid >= MINIMUM_USER_UID and uid in avail_gids:
                    return uid
                continue
        except ldap.TIMEOUT:
            raise ConnectionException(BACKEND_TIMEOUT)
        except AssertionError:
            raise ConnectionException(ASSERTION_FAILED)

    def create_account(self, uid, email, fullname, forcePass=None, requireTwo=True):
        """ Attempts to create a committer account in LDAP """
        if not self.isAdmin:
            raise ConnectionException('You do not have sufficient access to create accounts')
        if not LDAP_VALID_UID_RE.match(uid):
            raise ValidatorException('Invalid UID, must match ^[a-z0-9][a-z0-9_]+$')
        if self.load_account(uid):
            raise ConnectionException('An account with this uid already exists')
        res = self.lc.search_s(LDAP_SUFFIX, ldap.SCOPE_SUBTREE, 'cn=%s' % uid)
        if res:
            raise ValidatorException('availid clashes with project name %s!' % res[0][0], 'uid')
        uidnumber = self.next_user_uid()
        names = fullname.split(' ')
        if len(names) < 2 and requireTwo:
            raise ValidatorException('Full name needs at least two parts!', 'fullname')
        givenName = names[0]
        surName = names[-1]
        for n in names:
            if not n.strip():
                raise ValidatorException('Found part of name with too much spacing!', 'fullname')
        if not re.match('^\\S+@\\S+?\\.\\S+$', email):
            raise ValidatorException('Invalid email address supplied!', 'email')
        password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(16)))
        if forcePass:
            password = forcePass
        password_crypted = crypt.crypt(password, crypt.mksalt(method=crypt.METHOD_MD5))
        ldiff = {'objectClass': ['person', 'top', 'posixAccount', 'organizationalPerson', 'inetOrgPerson', 'asf-committer', 'hostObject', 'ldapPublicKey'], 'loginShell': '/bin/bash', 'asf-sascore': '10', 'givenName': givenName, 'sn': surName, 'mail': email, 'gidNumber': '9000', 'uidNumber': str(uidnumber), 'asf-committer-email': '%s@apache.org' % uid, 'cn': fullname, 'homeDirectory': '/home/%s' % uid, 'userPassword': '{CRYPT}' + password_crypted, 'host': 'home.apache.org'}
        bytify(ldiff)
        dn = LDAP_DN % uid
        am = ldap.modlist.addModlist(ldiff)
        self.lc.add_s(dn, am)
        return self.load_account(uid)

class LDIFWriter_Sane(ldif.LDIFWriter):
    """
    LDIFWriter with b64 detection overridden to allow for use of utf-8 rather than bytes
    Also disables b64 encoding for the 'dn' attribute
    """

    def _needs_base64_encoding(self, attr_type, attr_value):
        """
        returns False if attr_type is 'dn'
        returns True if attr_value has to be base-64 encoded because
        of special chars or because attr_type is in self._base64_attrs
        """
        if attr_type.lower() == 'dn':
            return False
        if type(attr_value) is bytes:
            return super()._needs_base64_encoding(attr_type, attr_value)
        if attr_type.lower() in self._base64_attrs:
            return True
        try:
            return super()._needs_base64_encoding(attr_type, attr_value.encode('utf-8'))
        except UnicodeEncodeError:
            return False