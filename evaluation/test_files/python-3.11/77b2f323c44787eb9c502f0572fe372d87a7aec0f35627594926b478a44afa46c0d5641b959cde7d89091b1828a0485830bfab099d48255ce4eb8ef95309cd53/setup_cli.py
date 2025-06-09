"""
this packages just what the CLI needs
"""
import fnmatch
import subprocess
from os import path
from typing import Any, Dict
from setuptools.command.build_py import build_py as build_py_orig
from setuptools import setup, find_packages

def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
        return dict((tuple(line.replace('\n', '').split('=')) for line in f.readlines() if not line.startswith('#')))
here = path.abspath(path.dirname(__file__))
try:
    p = subprocess.Popen('git rev-parse --short HEAD'.split(' '), stdout=subprocess.PIPE)
    if p.stdout:
        revision = p.stdout.readline().decode().strip()
    cli_config = get_env_data_as_dict('cli.env')
except Exception:
    revision = 'dev'
cli_info_file = f"\n__name__ = '{cli_config['CLI_NAME']}'\n__description__ = '{cli_config['CLI_DESCRIPTION']}'\n__url__ = '{cli_config['CLI_URL']}'\n__author__ = '{cli_config['CLI_AUTHOR']}'\n__author_email__ = '{cli_config['CLI_AUTHOR_EMAIL']}'\n__version__ = '{cli_config['CLI_VERSION']}'\n__revision__ = '{revision}'\n"
with open(path.join(here, 'tinybird', '__cli__.py'), 'w') as f:
    f.write(cli_info_file)
about: Dict[str, Any] = {}
with open(path.join(here, 'tinybird', '__cli__.py')) as f:
    exec(f.read(), about)
with open(path.join(here, 'cli_changelog.rst')) as f:
    readme = f.read()
included = ['tinybird/check_pypi.py', 'tinybird/ch_utils/constants.py', 'tinybird/ch_utils/engine.py', 'tinybird/client.py', 'tinybird/__cli__.py', 'tinybird/config.py', 'tinybird/connectors.py', 'tinybird/datafile.py', 'tinybird/datatypes.py', 'tinybird/feedback_manager.py', 'tinybird/sql.py', 'tinybird/context.py', 'tinybird/tornado_template.py', 'tinybird/sql_template.py', 'tinybird/sql_template_fmt.py', 'tinybird/sql_toolset.py', 'tinybird/syncasync.py', 'tinybird/tb_cli_modules/tinyunit/tinyunit.py', 'tinybird/tb_cli_modules/tinyunit/tinyunit_lib.py', 'tinybird/tb_cli_modules/common.py', 'tinybird/tb_cli_modules/auth.py', 'tinybird/tb_cli_modules/cli.py', 'tinybird/tb_cli_modules/connection.py', 'tinybird/tb_cli_modules/datasource.py', 'tinybird/tb_cli_modules/job.py', 'tinybird/tb_cli_modules/pipe.py', 'tinybird/tb_cli_modules/test.py', 'tinybird/tb_cli_modules/branch.py', 'tinybird/tb_cli_modules/workspace.py', 'tinybird/tb_cli_modules/workspace_members.py', 'tinybird/tb_cli.py']

class build_py(build_py_orig):

    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        files = [(pkg, mod, file) for pkg, mod, file in modules if any((fnmatch.fnmatchcase(file, pat=pattern) for pattern in included))]
        return files
setup(cmdclass={'build_py': build_py}, name=about['__name__'], version=about['__version__'], description=about['__description__'], long_description=readme, long_description_content_type='text/x-rst', url=about['__url__'], author=about['__author__'], author_email=about['__author_email__'], packages=find_packages(), python_requires='>=3.7, <3.11', install_requires=['cydifflib==1.0.1', 'click==8.0', 'clickhouse-toolset==0.23.dev0', 'colorama==0.4.6', 'humanfriendly==8.2', 'requests==2.28.1', 'requests-toolbelt==0.10.1', 'shandy-sqlfmt==0.11.1', 'shandy-sqlfmt[jinjafmt]==0.11.1', 'tabulate==0.8.3', 'toposort==1.5', 'tornado==5.1.1', 'pyyaml==6.0', 'wheel'], extras_require={'bigquery': ['gsutil==4.58', 'google-api-python-client==2.0.2', 'google-auth==1.27.1', 'google-auth-httplib2==0.1.0', 'google-cloud-storage==2.4.0', 'google-cloud-bigquery==2.11.0'], 'snowflake': ['snowflake-connector-python==2.7.1', 'gsutil==4.58', 'google-api-python-client==2.0.2', 'google-auth==1.27.1', 'google-auth-httplib2==0.1.0', 'google-cloud-storage==2.4.0', 'oauth2client==3.0.0', 'chardet<4,>=3.0.2', 'pyOpenSSL<20.0.0,>=16.2.0']}, setup_requires=['pytest-runner'], entry_points={'console_scripts': ['tb=tinybird.tb_cli:cli']})