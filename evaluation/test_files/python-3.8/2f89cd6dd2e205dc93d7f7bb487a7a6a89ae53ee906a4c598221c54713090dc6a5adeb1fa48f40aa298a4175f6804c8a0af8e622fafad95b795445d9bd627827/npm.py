""" Contains wrappers for npm commands and tasks """
import devops_toolset.tools.cli as cli
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.core.CommandsCore import CommandsCore
from devops_toolset.project_types.node.commands import Commands as NodeCommands
from devops_toolset.project_types.node.Literals import Literals as NodeLiterals
from devops_toolset.core.app import App
app: App = App()
literals = LiteralsCore([NodeLiterals])
commands = CommandsCore([NodeCommands])

def convert_npm_extra_args(*args):
    """ Converts a list of variable args into extra args of a command -- <args> """
    if args[0]:
        return ' -- ' + ' '.join(args)
    return ''

def convert_npm_parameter_if_present(value: bool):
    """ Converts a boolean value to a --if-present string."""
    if value:
        return '--if-present'
    return ''

def convert_npm_parameter_silent(value: bool):
    """ Converts a boolean value to a --silent string."""
    if value:
        return '--silent'
    return ''

def run_script(command: str, silent: bool=False, if_present: bool=False, *args):
    """ Wrapper for running arbitrary package scripts

    See Also:
        https://docs.npmjs.com/cli-commands/run-script.html
    Args:

        command: Command to run.
        silent: Prevents showing npm ERR! output on error.
        if_present: Prevents exiting with a non-zero exit code when the script is undefined.
        *args: Extra parameters will be passed as arguments to the subyacent npm run command.
    """
    cli.call_subprocess(commands.get('npm_run').format(command=command, silent=convert_npm_parameter_silent(silent), if_present=convert_npm_parameter_if_present(if_present), extra_args=convert_npm_extra_args(args)), log_before_out=[literals.get('npm_run_before').format(task=command)], log_after_out=[literals.get('npm_run_after').format(task=command)], log_after_err=[literals.get('npm_run_error').format(task=command)])

def install(folder: str=''):
    """ Installs a package, and any packages that it depends on

    See Also:
        https://docs.npmjs.com/cli/install

    Args:
        folder: Install the package in the directory as a symlink in the current project

    """
    cli.call_subprocess(commands.get('npm_install').format(folder=folder), log_before_out=[literals.get('npm_install_before')], log_after_out=[literals.get('npm_install_after')], log_after_err=[literals.get('npm_install_error')])
if __name__ == '__main__':
    help(__name__)