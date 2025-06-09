from __future__ import absolute_import, division, print_function
__metaclass__ = type
DOCUMENTATION = "\n---\nmodule: java_cert\n\nshort_description: Uses keytool to import/remove certificate to/from java keystore (cacerts)\ndescription:\n  - This is a wrapper module around keytool, which can be used to import certificates\n    and optionally private keys to a given java keystore, or remove them from it.\nextends_documentation_fragment:\n  - community.general.attributes\nattributes:\n  check_mode:\n    support: full\n  diff_mode:\n    support: full\noptions:\n  cert_url:\n    description:\n      - Basic URL to fetch SSL certificate from.\n      - Exactly one of C(cert_url), C(cert_path) or C(pkcs12_path) is required to load certificate.\n    type: str\n  cert_port:\n    description:\n      - Port to connect to URL.\n      - This will be used to create server URL:PORT.\n    type: int\n    default: 443\n  cert_path:\n    description:\n      - Local path to load certificate from.\n      - Exactly one of C(cert_url), C(cert_path) or C(pkcs12_path) is required to load certificate.\n    type: path\n  cert_alias:\n    description:\n      - Imported certificate alias.\n      - The alias is used when checking for the presence of a certificate in the keystore.\n    type: str\n  trust_cacert:\n    description:\n      - Trust imported cert as CAcert.\n    type: bool\n    default: false\n    version_added: '0.2.0'\n  pkcs12_path:\n    description:\n      - Local path to load PKCS12 keystore from.\n      - Unlike C(cert_url) and C(cert_path), the PKCS12 keystore embeds the private key matching\n        the certificate, and is used to import both the certificate and its private key into the\n        java keystore.\n      - Exactly one of C(cert_url), C(cert_path) or C(pkcs12_path) is required to load certificate.\n    type: path\n  pkcs12_password:\n    description:\n      - Password for importing from PKCS12 keystore.\n    type: str\n  pkcs12_alias:\n    description:\n      - Alias in the PKCS12 keystore.\n    type: str\n  keystore_path:\n    description:\n      - Path to keystore.\n    type: path\n  keystore_pass:\n    description:\n      - Keystore password.\n    type: str\n    required: true\n  keystore_create:\n    description:\n      - Create keystore if it does not exist.\n    type: bool\n    default: false\n  keystore_type:\n    description:\n      - Keystore type (JCEKS, JKS).\n    type: str\n  executable:\n    description:\n      - Path to keytool binary if not used we search in PATH for it.\n    type: str\n    default: keytool\n  state:\n    description:\n      - Defines action which can be either certificate import or removal.\n      - When state is present, the certificate will always idempotently be inserted\n        into the keystore, even if there already exists a cert alias that is different.\n    type: str\n    choices: [ absent, present ]\n    default: present\nrequirements: [openssl, keytool]\nauthor:\n- Adam Hamsik (@haad)\n"
EXAMPLES = '\n- name: Import SSL certificate from google.com to a given cacerts keystore\n  community.general.java_cert:\n    cert_url: google.com\n    cert_port: 443\n    keystore_path: /usr/lib/jvm/jre7/lib/security/cacerts\n    keystore_pass: changeit\n    state: present\n\n- name: Remove certificate with given alias from a keystore\n  community.general.java_cert:\n    cert_url: google.com\n    keystore_path: /usr/lib/jvm/jre7/lib/security/cacerts\n    keystore_pass: changeit\n    executable: /usr/lib/jvm/jre7/bin/keytool\n    state: absent\n\n- name: Import trusted CA from SSL certificate\n  community.general.java_cert:\n    cert_path: /opt/certs/rootca.crt\n    keystore_path: /tmp/cacerts\n    keystore_pass: changeit\n    keystore_create: true\n    state: present\n    cert_alias: LE_RootCA\n    trust_cacert: true\n\n- name: Import SSL certificate from google.com to a keystore, create it if it doesn\'t exist\n  community.general.java_cert:\n    cert_url: google.com\n    keystore_path: /tmp/cacerts\n    keystore_pass: changeit\n    keystore_create: true\n    state: present\n\n- name: Import a pkcs12 keystore with a specified alias, create it if it doesn\'t exist\n  community.general.java_cert:\n    pkcs12_path: "/tmp/importkeystore.p12"\n    cert_alias: default\n    keystore_path: /opt/wildfly/standalone/configuration/defaultkeystore.jks\n    keystore_pass: changeit\n    keystore_create: true\n    state: present\n\n- name: Import SSL certificate to JCEKS keystore\n  community.general.java_cert:\n    pkcs12_path: "/tmp/importkeystore.p12"\n    pkcs12_alias: default\n    pkcs12_password: somepass\n    cert_alias: default\n    keystore_path: /opt/someapp/security/keystore.jceks\n    keystore_type: "JCEKS"\n    keystore_pass: changeit\n    keystore_create: true\n    state: present\n'
RETURN = '\nmsg:\n  description: Output from stdout of keytool command after execution of given command.\n  returned: success\n  type: str\n  sample: "Module require existing keystore at keystore_path \'/tmp/test/cacerts\'"\n\nrc:\n  description: Keytool command execution return value.\n  returned: success\n  type: int\n  sample: "0"\n\ncmd:\n  description: Executed command to get action done.\n  returned: success\n  type: str\n  sample: "keytool -importcert -noprompt -keystore"\n'
import os
import tempfile
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves.urllib.parse import urlparse
from ansible.module_utils.six.moves.urllib.request import getproxies

def _get_keystore_type_keytool_parameters(keystore_type):
    """ Check that custom keystore is presented in parameters """
    if keystore_type:
        return ['-storetype', keystore_type]
    return []

def _check_cert_present(module, executable, keystore_path, keystore_pass, alias, keystore_type):
    """ Check if certificate with alias is present in keystore
        located at keystore_path """
    test_cmd = [executable, '-list', '-keystore', keystore_path, '-alias', alias, '-rfc']
    test_cmd += _get_keystore_type_keytool_parameters(keystore_type)
    check_rc, stdout, dummy = module.run_command(test_cmd, data=keystore_pass, check_rc=False)
    if check_rc == 0:
        return (True, stdout)
    return (False, '')

def _get_certificate_from_url(module, executable, url, port, pem_certificate_output):
    remote_cert_pem_chain = _download_cert_url(module, executable, url, port)
    with open(pem_certificate_output, 'w') as f:
        f.write(remote_cert_pem_chain)

def _get_first_certificate_from_x509_file(module, pem_certificate_file, pem_certificate_output, openssl_bin):
    """ Read a X509 certificate chain file and output the first certificate in the list """
    extract_cmd = [openssl_bin, 'x509', '-in', pem_certificate_file, '-out', pem_certificate_output]
    extract_rc, dummy, extract_stderr = module.run_command(extract_cmd, check_rc=False)
    if extract_rc != 0:
        extract_cmd += ['-inform', 'der']
        extract_rc, dummy, extract_stderr = module.run_command(extract_cmd, check_rc=False)
        if extract_rc != 0:
            module.fail_json(msg='Internal module failure, cannot extract certificate, error: %s' % extract_stderr, rc=extract_rc, cmd=extract_cmd)
    return extract_rc

def _get_digest_from_x509_file(module, pem_certificate_file, openssl_bin):
    """ Read a X509 certificate file and output sha256 digest using openssl """
    dummy, tmp_certificate = tempfile.mkstemp()
    module.add_cleanup_file(tmp_certificate)
    _get_first_certificate_from_x509_file(module, pem_certificate_file, tmp_certificate, openssl_bin)
    dgst_cmd = [openssl_bin, 'dgst', '-r', '-sha256', tmp_certificate]
    dgst_rc, dgst_stdout, dgst_stderr = module.run_command(dgst_cmd, check_rc=False)
    if dgst_rc != 0:
        module.fail_json(msg='Internal module failure, cannot compute digest for certificate, error: %s' % dgst_stderr, rc=dgst_rc, cmd=dgst_cmd)
    return dgst_stdout.split(' ')[0]

def _export_public_cert_from_pkcs12(module, executable, pkcs_file, alias, password, dest):
    """ Runs keytools to extract the public cert from a PKCS12 archive and write it to a file. """
    export_cmd = [executable, '-list', '-noprompt', '-keystore', pkcs_file, '-alias', alias, '-storetype', 'pkcs12', '-rfc']
    export_rc, export_stdout, export_err = module.run_command(export_cmd, data=password, check_rc=False)
    if export_rc != 0:
        module.fail_json(msg='Internal module failure, cannot extract public certificate from PKCS12, message: %s' % export_stdout, stderr=export_err, rc=export_rc)
    with open(dest, 'w') as f:
        f.write(export_stdout)

def get_proxy_settings(scheme='https'):
    """ Returns a tuple containing (proxy_host, proxy_port). (False, False) if no proxy is found """
    proxy_url = getproxies().get(scheme, '')
    if not proxy_url:
        return (False, False)
    else:
        parsed_url = urlparse(proxy_url)
        if parsed_url.scheme:
            proxy_host, proxy_port = parsed_url.netloc.split(':')
        else:
            proxy_host, proxy_port = parsed_url.path.split(':')
        return (proxy_host, proxy_port)

def build_proxy_options():
    """ Returns list of valid proxy options for keytool """
    proxy_host, proxy_port = get_proxy_settings()
    no_proxy = os.getenv('no_proxy')
    proxy_opts = []
    if proxy_host:
        proxy_opts.extend(['-J-Dhttps.proxyHost=%s' % proxy_host, '-J-Dhttps.proxyPort=%s' % proxy_port])
        if no_proxy is not None:
            non_proxy_hosts = no_proxy.replace(',', '|')
            non_proxy_hosts = re.sub('(^|\\|)\\.', '\\1*.', non_proxy_hosts)
            proxy_opts.extend(['-J-Dhttp.nonProxyHosts=%s' % non_proxy_hosts])
    return proxy_opts

def _download_cert_url(module, executable, url, port):
    """ Fetches the certificate from the remote URL using `keytool -printcert...`
          The PEM formatted string is returned """
    proxy_opts = build_proxy_options()
    fetch_cmd = [executable, '-printcert', '-rfc', '-sslserver'] + proxy_opts + ['%s:%d' % (url, port)]
    fetch_rc, fetch_out, fetch_err = module.run_command(fetch_cmd, check_rc=False)
    if fetch_rc != 0:
        module.fail_json(msg='Internal module failure, cannot download certificate, error: %s' % fetch_err, rc=fetch_rc, cmd=fetch_cmd)
    return fetch_out

def import_pkcs12_path(module, executable, pkcs12_path, pkcs12_pass, pkcs12_alias, keystore_path, keystore_pass, keystore_alias, keystore_type):
    """ Import pkcs12 from path into keystore located on
        keystore_path as alias """
    import_cmd = [executable, '-importkeystore', '-noprompt', '-srcstoretype', 'pkcs12', '-srckeystore', pkcs12_path, '-srcalias', pkcs12_alias, '-destkeystore', keystore_path, '-destalias', keystore_alias]
    import_cmd += _get_keystore_type_keytool_parameters(keystore_type)
    secret_data = '%s\n%s' % (keystore_pass, pkcs12_pass)
    if not os.path.exists(keystore_path):
        secret_data = '%s\n%s' % (keystore_pass, secret_data)
    import_rc, import_out, import_err = module.run_command(import_cmd, data=secret_data, check_rc=False)
    diff = {'before': '\n', 'after': '%s\n' % keystore_alias}
    if import_rc == 0 and os.path.exists(keystore_path):
        module.exit_json(changed=True, msg=import_out, rc=import_rc, cmd=import_cmd, stdout=import_out, error=import_err, diff=diff)
    else:
        module.fail_json(msg=import_out, rc=import_rc, cmd=import_cmd, error=import_err)

def import_cert_path(module, executable, path, keystore_path, keystore_pass, alias, keystore_type, trust_cacert):
    """ Import certificate from path into keystore located on
        keystore_path as alias """
    import_cmd = [executable, '-importcert', '-noprompt', '-keystore', keystore_path, '-file', path, '-alias', alias]
    import_cmd += _get_keystore_type_keytool_parameters(keystore_type)
    if trust_cacert:
        import_cmd.extend(['-trustcacerts'])
    import_rc, import_out, import_err = module.run_command(import_cmd, data='%s\n%s' % (keystore_pass, keystore_pass), check_rc=False)
    diff = {'before': '\n', 'after': '%s\n' % alias}
    if import_rc == 0:
        module.exit_json(changed=True, msg=import_out, rc=import_rc, cmd=import_cmd, stdout=import_out, error=import_err, diff=diff)
    else:
        module.fail_json(msg=import_out, rc=import_rc, cmd=import_cmd)

def delete_cert(module, executable, keystore_path, keystore_pass, alias, keystore_type, exit_after=True):
    """ Delete certificate identified with alias from keystore on keystore_path """
    del_cmd = [executable, '-delete', '-noprompt', '-keystore', keystore_path, '-alias', alias]
    del_cmd += _get_keystore_type_keytool_parameters(keystore_type)
    del_rc, del_out, del_err = module.run_command(del_cmd, data=keystore_pass, check_rc=True)
    if exit_after:
        diff = {'before': '%s\n' % alias, 'after': None}
        module.exit_json(changed=True, msg=del_out, rc=del_rc, cmd=del_cmd, stdout=del_out, error=del_err, diff=diff)

def test_keytool(module, executable):
    """ Test if keytool is actually executable or not """
    module.run_command([executable], check_rc=True)

def test_keystore(module, keystore_path):
    """ Check if we can access keystore as file or not """
    if keystore_path is None:
        keystore_path = ''
    if not os.path.exists(keystore_path) and (not os.path.isfile(keystore_path)):
        module.fail_json(changed=False, msg="Module require existing keystore at keystore_path '%s'" % keystore_path)

def main():
    argument_spec = dict(cert_url=dict(type='str'), cert_path=dict(type='path'), pkcs12_path=dict(type='path'), pkcs12_password=dict(type='str', no_log=True), pkcs12_alias=dict(type='str'), cert_alias=dict(type='str'), cert_port=dict(type='int', default=443), keystore_path=dict(type='path'), keystore_pass=dict(type='str', required=True, no_log=True), trust_cacert=dict(type='bool', default=False), keystore_create=dict(type='bool', default=False), keystore_type=dict(type='str'), executable=dict(type='str', default='keytool'), state=dict(type='str', default='present', choices=['absent', 'present']))
    module = AnsibleModule(argument_spec=argument_spec, required_if=[['state', 'present', ('cert_path', 'cert_url', 'pkcs12_path'), True], ['state', 'absent', ('cert_url', 'cert_alias'), True]], required_together=[['keystore_path', 'keystore_pass']], mutually_exclusive=[['cert_url', 'cert_path', 'pkcs12_path']], supports_check_mode=True)
    url = module.params.get('cert_url')
    path = module.params.get('cert_path')
    port = module.params.get('cert_port')
    pkcs12_path = module.params.get('pkcs12_path')
    pkcs12_pass = module.params.get('pkcs12_password', '')
    pkcs12_alias = module.params.get('pkcs12_alias', '1')
    cert_alias = module.params.get('cert_alias') or url
    trust_cacert = module.params.get('trust_cacert')
    keystore_path = module.params.get('keystore_path')
    keystore_pass = module.params.get('keystore_pass')
    keystore_create = module.params.get('keystore_create')
    keystore_type = module.params.get('keystore_type')
    executable = module.params.get('executable')
    state = module.params.get('state')
    openssl_bin = module.get_bin_path('openssl', True)
    if path and (not cert_alias):
        module.fail_json(changed=False, msg='Using local path import from %s requires alias argument.' % keystore_path)
    test_keytool(module, executable)
    if not keystore_create:
        test_keystore(module, keystore_path)
    alias_exists, alias_exists_output = _check_cert_present(module, executable, keystore_path, keystore_pass, cert_alias, keystore_type)
    dummy, new_certificate = tempfile.mkstemp()
    dummy, old_certificate = tempfile.mkstemp()
    module.add_cleanup_file(new_certificate)
    module.add_cleanup_file(old_certificate)
    if state == 'absent' and alias_exists:
        if module.check_mode:
            module.exit_json(changed=True)
        delete_cert(module, executable, keystore_path, keystore_pass, cert_alias, keystore_type)
    if state == 'present':
        if alias_exists:
            with open(old_certificate, 'w') as f:
                f.write(alias_exists_output)
            keystore_cert_digest = _get_digest_from_x509_file(module, old_certificate, openssl_bin)
        else:
            keystore_cert_digest = ''
        if pkcs12_path:
            _export_public_cert_from_pkcs12(module, executable, pkcs12_path, pkcs12_alias, pkcs12_pass, new_certificate)
        elif path:
            new_certificate = path
        elif url:
            _get_certificate_from_url(module, executable, url, port, new_certificate)
        new_cert_digest = _get_digest_from_x509_file(module, new_certificate, openssl_bin)
        if keystore_cert_digest != new_cert_digest:
            if module.check_mode:
                module.exit_json(changed=True)
            if alias_exists:
                delete_cert(module, executable, keystore_path, keystore_pass, cert_alias, keystore_type, exit_after=False)
            if pkcs12_path:
                import_pkcs12_path(module, executable, pkcs12_path, pkcs12_pass, pkcs12_alias, keystore_path, keystore_pass, cert_alias, keystore_type)
            else:
                import_cert_path(module, executable, new_certificate, keystore_path, keystore_pass, cert_alias, keystore_type, trust_cacert)
    module.exit_json(changed=False)
if __name__ == '__main__':
    main()