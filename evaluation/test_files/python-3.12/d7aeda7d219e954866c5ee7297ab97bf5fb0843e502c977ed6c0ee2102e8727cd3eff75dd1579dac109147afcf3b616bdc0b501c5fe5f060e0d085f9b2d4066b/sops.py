from __future__ import absolute_import, division, print_function
__metaclass__ = type
import os
from ansible.module_utils.common.text.converters import to_text, to_native
from subprocess import Popen, PIPE
SOPS_ERROR_CODES = {1: 'ErrorGeneric', 2: 'CouldNotReadInputFile', 3: 'CouldNotWriteOutputFile', 4: 'ErrorDumpingTree', 5: 'ErrorReadingConfig', 6: 'ErrorInvalidKMSEncryptionContextFormat', 7: 'ErrorInvalidSetFormat', 8: 'ErrorConflictingParameters', 21: 'ErrorEncryptingMac', 23: 'ErrorEncryptingTree', 24: 'ErrorDecryptingMac', 25: 'ErrorDecryptingTree', 49: 'CannotChangeKeysFromNonExistentFile', 51: 'MacMismatch', 52: 'MacNotFound', 61: 'ConfigFileNotFound', 85: 'KeyboardInterrupt', 91: 'InvalidTreePathFormat', 100: 'NoFileSpecified', 128: 'CouldNotRetrieveKey', 111: 'NoEncryptionKeyFound', 200: 'FileHasNotBeenModified', 201: 'NoEditorFound', 202: 'FailedToCompareVersions', 203: 'FileAlreadyEncrypted'}

def _create_single_arg(argument_name):

    def f(value, arguments, env):
        arguments.extend([argument_name, to_native(value)])
    return f

def _create_comma_separated(argument_name):

    def f(value, arguments, env):
        arguments.extend([argument_name, ','.join([to_native(v) for v in value])])
    return f

def _create_repeated(argument_name):

    def f(value, arguments, env):
        for v in value:
            arguments.extend([argument_name, to_native(v)])
    return f

def _create_boolean(argument_name):

    def f(value, arguments, env):
        if value:
            arguments.append(argument_name)
    return f

def _create_env_variable(argument_name):

    def f(value, arguments, env):
        env[argument_name] = value
    return f
GENERAL_OPTIONS = {'age_key': _create_env_variable('SOPS_AGE_KEY'), 'age_keyfile': _create_env_variable('SOPS_AGE_KEY_FILE'), 'aws_profile': _create_single_arg('--aws-profile'), 'aws_access_key_id': _create_env_variable('AWS_ACCESS_KEY_ID'), 'aws_secret_access_key': _create_env_variable('AWS_SECRET_ACCESS_KEY'), 'aws_session_token': _create_env_variable('AWS_SESSION_TOKEN'), 'config_path': _create_single_arg('--config'), 'enable_local_keyservice': _create_boolean('--enable-local-keyservice'), 'keyservice': _create_repeated('--keyservice')}
ENCRYPT_OPTIONS = {'age': _create_comma_separated('--age'), 'kms': _create_comma_separated('--kms'), 'gcp_kms': _create_comma_separated('--gcp-kms'), 'azure_kv': _create_comma_separated('--azure-kv'), 'hc_vault_transit': _create_comma_separated('--hc-vault-transit'), 'pgp': _create_comma_separated('--pgp'), 'unencrypted_suffix': _create_single_arg('--unencrypted-suffix'), 'encrypted_suffix': _create_single_arg('--encrypted-suffix'), 'unencrypted_regex': _create_single_arg('--unencrypted-regex'), 'encrypted_regex': _create_single_arg('--encrypted-regex'), 'encryption_context': _create_comma_separated('--encryption-context'), 'shamir_secret_sharing_threshold': _create_single_arg('--shamir-secret-sharing-threshold')}

class SopsError(Exception):
    """ Extend Exception class with sops specific informations """

    def __init__(self, filename, exit_code, message, decryption=True):
        if exit_code in SOPS_ERROR_CODES:
            exception_name = SOPS_ERROR_CODES[exit_code]
            message = 'error with file %s: %s exited with code %d: %s' % (filename, exception_name, exit_code, to_native(message))
        else:
            message = 'could not %s file %s; Unknown sops error code: %s; message: %s' % ('decrypt' if decryption else 'encrypt', filename, exit_code, to_native(message))
        super(SopsError, self).__init__(message)

class Sops:
    """ Utility class to perform sops CLI actions """

    @staticmethod
    def _add_options(command, env, get_option_value, options):
        if get_option_value is None:
            return
        for option, f in options.items():
            v = get_option_value(option)
            if v is not None:
                f(v, command, env)

    @staticmethod
    def get_sops_binary(get_option_value):
        cmd = get_option_value('sops_binary') if get_option_value else None
        if cmd is None:
            cmd = 'sops'
        return cmd

    @staticmethod
    def decrypt(encrypted_file, content=None, display=None, decode_output=True, rstrip=True, input_type=None, output_type=None, get_option_value=None, module=None):
        command = [Sops.get_sops_binary(get_option_value)]
        env = os.environ.copy()
        Sops._add_options(command, env, get_option_value, GENERAL_OPTIONS)
        if input_type is not None:
            command.extend(['--input-type', input_type])
        if output_type is not None:
            command.extend(['--output-type', output_type])
        if content is not None:
            encrypted_file = '/dev/stdin'
        command.extend(['--decrypt', encrypted_file])
        if module:
            exit_code, output, err = module.run_command(command, environ_update=env, encoding=None, data=content, binary_data=True)
        else:
            process = Popen(command, stdin=None if content is None else PIPE, stdout=PIPE, stderr=PIPE, env=env)
            output, err = process.communicate(input=content)
            exit_code = process.returncode
        if decode_output:
            output = to_text(output, errors='surrogate_or_strict')
        if err and display:
            display.vvvv(to_text(err, errors='surrogate_or_strict'))
        if exit_code != 0:
            raise SopsError(encrypted_file, exit_code, err, decryption=True)
        if rstrip:
            output = output.rstrip()
        return output

    @staticmethod
    def encrypt(data, display=None, cwd=None, input_type=None, output_type=None, get_option_value=None, module=None):
        command = [Sops.get_sops_binary(get_option_value)]
        env = os.environ.copy()
        Sops._add_options(command, env, get_option_value, GENERAL_OPTIONS)
        Sops._add_options(command, env, get_option_value, ENCRYPT_OPTIONS)
        if input_type is not None:
            command.extend(['--input-type', input_type])
        if output_type is not None:
            command.extend(['--output-type', output_type])
        command.extend(['--encrypt', '/dev/stdin'])
        if module:
            exit_code, output, err = module.run_command(command, data=data, binary_data=True, cwd=cwd, environ_update=env, encoding=None)
        else:
            process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env)
            output, err = process.communicate(input=data)
            exit_code = process.returncode
        if err and display:
            display.vvvv(to_text(err, errors='surrogate_or_strict'))
        if exit_code != 0:
            raise SopsError('to stdout', exit_code, err, decryption=False)
        return output

def get_sops_argument_spec(add_encrypt_specific=False):
    argument_spec = {'sops_binary': {'type': 'path'}, 'age_key': {'type': 'str', 'no_log': True}, 'age_keyfile': {'type': 'path'}, 'aws_profile': {'type': 'str'}, 'aws_access_key_id': {'type': 'str'}, 'aws_secret_access_key': {'type': 'str', 'no_log': True}, 'aws_session_token': {'type': 'str', 'no_log': True}, 'config_path': {'type': 'path'}, 'enable_local_keyservice': {'type': 'bool', 'default': False}, 'keyservice': {'type': 'list', 'elements': 'str'}}
    if add_encrypt_specific:
        argument_spec.update({'age': {'type': 'list', 'elements': 'str'}, 'kms': {'type': 'list', 'elements': 'str'}, 'gcp_kms': {'type': 'list', 'elements': 'str'}, 'azure_kv': {'type': 'list', 'elements': 'str'}, 'hc_vault_transit': {'type': 'list', 'elements': 'str'}, 'pgp': {'type': 'list', 'elements': 'str'}, 'unencrypted_suffix': {'type': 'str'}, 'encrypted_suffix': {'type': 'str'}, 'unencrypted_regex': {'type': 'str'}, 'encrypted_regex': {'type': 'str'}, 'encryption_context': {'type': 'list', 'elements': 'str'}, 'shamir_secret_sharing_threshold': {'type': 'int', 'no_log': False}})
    return argument_spec