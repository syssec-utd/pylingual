import uuid
from subprocess import PIPE, STDOUT
import hashlib
import requests
import stat
from contextlib import contextmanager
import re
import inquirer
import cProfile
import functools
try:
    import arrow
except ImportError:
    pass
from pathlib import Path
import io
import traceback
import json
import pipes
import tempfile
from datetime import datetime
try:
    from retrying import retry
except ImportError:
    retry = None
from .wait import tcp as tcp_wait
import shutil
try:
    import click
except ImportError:
    pass
import os
import subprocess
import time
import sys
from threading import Thread
from queue import Queue
import inspect
from copy import deepcopy
from passlib.context import CryptContext

class DBConnection(object):

    def __init__(self, dbname, host, port, user, pwd):
        assert dbname
        assert host
        assert user
        assert pwd
        self.dbname = dbname
        self.host = host
        self.port = int(port)
        self.user = user
        self.pwd = pwd

    def shortstr(self):
        return '{}:{}/{}'.format(self.host, self.port, self.dbname)

    def clone(self, dbname=None):
        result = deepcopy(self)
        if dbname:
            result.dbname = dbname
        return result

    def get_psyco_connection(self, db=None):
        import psycopg2
        while True:
            try:
                conn = psycopg2.connect(dbname=db or self.dbname, user=self.user, password=self.pwd, host=self.host, port=self.port or None, connect_timeout=int(os.getenv('PSYCOPG_TIMEOUT', '3')))
                break
            except psycopg2.OperationalError as ex:
                if 'database system is starting up' in str(ex):
                    time.sleep(2)
                else:
                    raise
        return conn

    @contextmanager
    def connect(self, db=None):
        conn = self.get_psyco_connection(db=db)
        cr = conn.cursor()
        try:
            yield cr
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            cr.close()
            conn.close()

def __assert_file_exists(path, isdir=False):
    if not Path(path).exists():
        raise Exception('{} {} not found!'.format('Directory' if isdir else 'File', path))

def __safe_filename(name):
    name = name or ''
    for c in [':\\/+?*;\'" ']:
        name = name.replace(c, '_')
    return name

def __write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)

def __concurrent_safe_write_file(file, content, as_string=True):
    tmpfilename = file.parent / (file.name + '.tmp.safewritefile')
    if tmpfilename.exists():
        tmpfilename.unlink()
    if as_string:
        tmpfilename.write_text(content)
    else:
        tmpfilename.write_bytes(content)
    if file.exists():
        file.unlink()
    shutil.move(tmpfilename, file)

def __append_line(path, line):
    if not Path(path).exists():
        content = ''
    else:
        with open(path, 'r') as f:
            content = f.read().strip()
    content += '\n' + line
    with open(path, 'w') as f:
        f.write(content)

def __read_file(path, error=True):
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        if not error:
            return ''

def E2(name):
    if name.startswith('$'):
        name = name[1:]
    return os.getenv(name, '')

def __get_odoo_commit():
    from .odoo_config import MANIFEST
    commit = MANIFEST().get('odoo-commit', '')
    if not commit:
        raise Exception('No odoo commit defined.')
    return commit

def _execute_sql(connection, sql, fetchone=False, fetchall=False, notransaction=False, no_try=False, params=None, return_columns=False):

    @retry(wait_random_min=500, wait_random_max=800, stop_max_delay=30000)
    def try_connect(connection):
        try:
            if hasattr(connection, 'clone'):
                connection = connection.clone(dbname='postgres')
            _execute_sql(connection, 'SELECT * FROM pg_catalog.pg_tables;', no_try=True)
        except Exception as e:
            click.secho(str(e), fg='red')
    if not no_try:
        try_connect(connection)

    def _call_cr(cr):
        cr.execute(sql, params)
        if fetchone:
            return cr.fetchone()
        elif fetchall:
            return cr.fetchall()
    if isinstance(connection, DBConnection):
        conn = connection.get_psyco_connection()
        conn.autocommit = notransaction
        cr = conn.cursor()
        try:
            res = _call_cr(cr)
            conn.commit()
            if return_columns:
                return ([x.name for x in cr.description], res)
            else:
                return res
        except Exception:
            conn.rollback()
            raise
        finally:
            cr.close()
            conn.close()
    else:
        return _call_cr(connection)

def _exists_db(conn):
    sql = f"select count(*) from pg_database where datname='{conn.dbname}'"
    conn = conn.clone()
    conn.dbname = 'postgres'
    record = _execute_sql(conn, sql, fetchone=True)
    if not record or not record[0]:
        return False
    return True

def _exists_table(conn, table_name):
    record = _execute_sql(conn, f"select exists(    select 1    from information_schema.tables    where table_name = '{table_name}' )", fetchone=True)
    return record[0]

def docker_list_containers(project_name, service_name, status_filter=None):
    cmd = ['docker', 'ps', '-a', '-q', '--no-trunc', '--filter', f'name=^/{project_name}_{service_name}$']
    if status_filter:
        cmd += ['--filter', f'status={status_filter}']
    container_ids = subprocess.check_output(cmd, encoding='utf8').strip().splitlines()
    return container_ids

def _wait_postgres(config, timeout=600):
    started = arrow.get()
    if config.run_postgres:
        conn = config.get_odoo_conn().clone(dbname='postgres')
        container_ids = subprocess.check_output(['docker', 'ps', '-a', '-q', '--no-trunc', '--filter', f'name=^/{config.PROJECT_NAME}_postgres$'], encoding='utf8').strip().splitlines()
        import docker
        client = docker.from_env()
        postgres_containers = []
        for container_id in container_ids:
            if not container_id:
                continue
            state = _docker_id_state(container_id)
            if state == 'running':
                postgres_containers += [container_id]
        deadline = arrow.get().shift(seconds=timeout)
        last_ex = None
        while True:
            if arrow.get() > deadline:
                if not postgres_containers:
                    abort("No running postgres container found. Perhaps you have to start it with 'odoo up -d postgres' first?")
                raise Exception(f'Timeout waiting postgres reached: {timeout}seconds')
            try:
                _execute_sql(conn, sql='\n                SELECT table_schema,table_name\n                FROM information_schema.tables\n                ORDER BY table_schema,table_name\n                LIMIT 1;\n                ')
                break
            except Exception as ex:
                seconds = (arrow.get() - started).total_seconds()
                if seconds > 5:
                    if str(ex) != str(last_ex):
                        click.secho(f'Waiting again for postgres. Last error is: {str(ex)}')
                    last_ex = ex
                time.sleep(1)
        click.secho('Postgres now available.', fg='green')

def _docker_id_state(container_id):
    status = subprocess.check_output(['docker', 'container', 'ls', '--format', '{{.State}}', '--filter', f'id={container_id}'], encoding='utf8').strip()
    return status

def docker_kill_container(container_id, remove=False):
    subprocess.check_call(['docker', 'kill', container_id])
    if remove:
        subprocess.check_call(['docker', 'rm', container_id])

def _is_container_running(config, machine_name):
    container_id = __dc_out(config, ['ps', '-q', machine_name]).strip()
    if container_id:
        status = _docker_id_state(container_id)
        if status:
            return status == 'running'
    return False

def is_up(config, *machine_name):
    assert len(machine_name) == 1
    click.echo('Running' if _is_container_running(config, machine_name[0]) else 'Not Running', machine_name[0])

def _isfloat(x):
    try:
        float(x)
    except Exception:
        return False
    else:
        return True

def _makedirs(path):
    path.mkdir(exist_ok=True, parents=True)

def _remove_postgres_connections(connection, sql_afterwards=''):
    click.echo(f'Removing all current connections from {connection.dbname}')
    if os.getenv('POSTGRES_DONT_DROP_ACTIVITIES', '') != '1':
        if _exists_db(connection):
            SQL = "\n                SELECT pg_terminate_backend(pg_stat_activity.pid)\n                FROM pg_stat_activity\n                WHERE pg_stat_activity.datname = '{}'\n                AND pid <> pg_backend_pid();\n            ".format(connection.dbname, sql_afterwards)
            _execute_sql(connection.clone(dbname='postgres'), SQL, notransaction=True)
            if sql_afterwards:
                _execute_sql(connection.clone(dbname='postgres'), sql_afterwards, notransaction=True)

def __rename_db_drop_target(conn, from_db, to_db):
    if to_db in ('postgres', 'template1'):
        raise Exception('Invalid: {}'.format(to_db))
    _remove_postgres_connections(conn.clone(dbname=from_db))
    _remove_postgres_connections(conn.clone(dbname=to_db))
    _execute_sql(conn.clone(dbname='postgres'), f'drop database if exists {to_db}', notransaction=True)
    _execute_sql(conn.clone(dbname='postgres'), f'alter database {from_db} rename to {to_db};', notransaction=True)
    _remove_postgres_connections(conn.clone(dbname=to_db))

def _merge_env_dict(env):
    res = {}
    for k, v in os.environ.items():
        res[k] = v
    for k, v in env.items():
        res[k] = v
    return res

def _set_default_envs(env):
    env = env or {}
    env.update({'DOCKER_BUILDKIT': '1', 'COMPOSE_DOCKER_CLI_BUILD': '1'})
    return env

def __dc(config, cmd, env={}):
    ensure_project_name(config)
    c = __get_cmd(config) + cmd
    env = _set_default_envs(env)
    return subprocess.check_call(c, env=_merge_env_dict(env))

def __dc_out(config, cmd, env={}):
    ensure_project_name(config)
    c = __get_cmd(config) + cmd
    env = _set_default_envs(env)
    return subprocess.check_output(c, env=_merge_env_dict(env))

def __dcexec(config, cmd, interactive=True, env=None):
    ensure_project_name(config)
    env = _set_default_envs(env)
    c = __get_cmd(config)
    c += ['exec']
    if not interactive:
        c += ['-T']
    if env:
        for k, v in env.items():
            c += ['-e', f'{k}={v}']
    c += cmd
    if interactive:
        subprocess.call(c)
    else:
        return subprocess.check_output(cmd)

def __dcrun(config, cmd, interactive=False, env={}, returncode=False, pass_stdin=None, returnproc=False):
    ensure_project_name(config)
    env = _set_default_envs(env)
    cmd2 = [os.path.expandvars(x) for x in cmd]
    cmd = ['run']
    if not interactive:
        cmd += ['-T']
    cmd += ['--rm']
    for k, v in env.items():
        cmd += ['-e{}={}'.format(k, v)]
    cmd += cmd2
    del cmd2
    cmd = __get_cmd(config) + cmd
    if interactive:
        optional_params = {}
        if pass_stdin:
            optional_params['input'] = pass_stdin
            optional_params['universal_newlines'] = True
        else:
            optional_params['stdin'] = sys.stdin
        return subprocess.run(cmd, check=True, **optional_params)
    elif returncode or returnproc:
        process = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = ''
        for line in iter(process.stdout.readline, b''):
            line = line.decode('utf-8').strip()
            print(line)
            output += line + '\n'
        process.communicate()
        process.wait()
        if returncode:
            return process.returncode
        return (process.returncode, output)
    else:
        optional_params = {}
        if pass_stdin:
            optional_params['input'] = pass_stdin
            optional_params['universal_newlines'] = True
        return subprocess.check_output(cmd, **optional_params)

def _askcontinue(config, msg=None):
    if msg:
        click.echo(msg)
    if config and config.force:
        return
    input('Continue? (Ctrl+C to break)')

def _wait_for_port(host, port, timeout=None):
    res = tcp_wait.open(port, host=host, timeout=timeout)
    if not res and timeout:
        raise Exception('Timeout elapsed waiting for {}:{}'.format(host, port))

def __replace_in_file(filepath, text, replacewith):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace(text, replacewith)
    with open(filepath, 'w') as f:
        f.write(content)

def __rm_file_if_exists(path):
    if path.exists():
        path.unlink()

def __rmtree(config, path):
    path = str(path)
    if not path or path == '/':
        raise Exception('Not allowed: {}'.format(path))
    if not path.startswith('/'):
        raise Exception('Not allowed: {}'.format(path))
    if config:
        if not any((path.startswith(config.dirs['odoo_home'] + x) for x in ['/tmp', '/run/'])):
            if '/tmp' in path:
                pass
            else:
                raise Exception('not allowed')
    if Path(path).exists():
        shutil.rmtree(path)

def __safeget(array, index, exception_on_missing, file_options=None):
    if file_options:
        if file_options.exists():
            file_options = '\n' + '\n'.join(file_options.glob('*'))
    file_options = file_options or ''
    if len(array) < index + 1:
        raise Exception(exception_on_missing + file_options)
    return array[index]

def __get_cmd(config):
    cmd = config.commands['dc']
    cmd = [os.path.expandvars(x) for x in cmd]
    return cmd

def __cmd_interactive(config, *params, return_proc=False):
    cmd = __get_cmd(config) + list(params)
    proc = subprocess.Popen(cmd)
    proc.wait()
    if return_proc:
        return proc
    return proc.returncode

def __empty_dir(dir, user_out=False):
    dir = Path(dir)
    try:
        for x in dir.glob('*'):
            if x.is_dir():
                if user_out:
                    click.secho(f'Removing {x.absolute()}')
                shutil.rmtree(x.absolute())
            else:
                if user_out:
                    click.secho(f'Removing {x.absolute()}')
                x.unlink()
    except:
        click.secho(f'Could not delete: {dir}', fg='red')
        raise

def __file_default_content(path, default_content):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(default_content)

def __file_get_lines(path):
    return path.read_text().strip().splitlines()

def _get_machines(config):
    cmd = config.commands['dc'] + ['ps', '--services']
    out = subprocess.check_output(cmd, cwd=config.dirs['odoo_home'])
    out = set(filter(lambda x: x, out.splitlines()))
    return list(sorted(out))
if retry:

    @retry(wait_random_min=500, wait_random_max=800, stop_max_delay=30000)
    def __get_docker_image():
        """
        Sometimes this command fails; checked with pudb behind call, hostname matches
        container id; seems to be race condition or so
        """
        hostname = os.environ['HOSTNAME']
        result = [x for x in subprocess.check_output(['/opt/docker/docker', 'inspect', hostname]).splitlines() if '"Image"' in x]
        if result:
            result = result[0].split('sha256:')[-1].split('"')[0]
            return result[:12]
        return None

def _file2env(filepath, out_dict=None):
    from . import MyConfigParser
    if not filepath.exists():
        return
    config = MyConfigParser(filepath)
    for k in config.keys():
        if out_dict:
            out_dict[k] = config[k]
        else:
            os.environ[k] = config[k]

def _get_bash_for_machine(machine):
    return 'bash'

def __get_installed_modules(config):
    conn = config.get_odoo_conn()
    rows = _execute_sql(conn, sql="SELECT name, state from ir_module_module where state in ('installed', 'to upgrade');", fetchall=True)
    return [x[0] for x in rows]

def __splitcomma(param):
    if isinstance(param, str):
        if not param:
            return []
        return [x.strip() for x in param.split(',') if x.strip()]
    elif isinstance(param, (tuple, list)):
        return list(param)
    raise Exception('not impl')

def __make_file_executable(filepath):
    st = os.stat(filepath)
    os.chmod(filepath, st.st_mode | stat.S_IEXEC)

def _get_user_primary_group(UID):
    id = search_env_path('id')
    return subprocess.check_output([id, '-gn', str(UID)], encoding='utf8').strip()

def __try_to_set_owner(UID, path, abort_if_failed=True, verbose=False):
    primary_group = _get_user_primary_group(UID)
    find_command = f"find '{path}' -not -type l -not -user {UID}"
    res = subprocess.check_output(find_command, encoding='utf8', shell=True).strip().splitlines()
    find_command = f"find '{path}' -not -type l -not -group {primary_group}"
    res += subprocess.check_output(find_command, encoding='utf8', shell=True).strip().splitlines()
    res = sorted(list(res))
    if not res:
        return
    for line in filter(bool, res):
        try:
            try:
                subprocess.check_output(['chown', str(UID), line])
            except:
                try:
                    subprocess.check_output(['sudo', 'chown', str(UID), line])
                except Exception as ex:
                    if abort_if_failed:
                        abort(f'Could not set owner {UID} on path {line}; \n\n{ex}')
            try:
                subprocess.check_output(['chgrp', str(primary_group), line])
            except:
                try:
                    subprocess.check_output(['sudo', 'chgrp', str(primary_group), line])
                except:
                    pass
        except FileNotFoundError:
            continue
        else:
            if verbose:
                click.secho(f'Setting ownership {UID} on {line}')

def _display_machine_tips(config, machine_name):
    dir = config.dirs['images'] / machine_name
    if not dir.is_dir():
        return
    for filename in config.dirs['images'].glob('**/tips.txt'):
        filepath = config.dirs['images'] / filename
        if filepath.parent.name == machine_name:
            content = (config.dirs['images'] / filename).read_text()
            click.echo('')
            click.echo('Please note:')
            click.echo('---------------')
            click.echo('')
            click.echo(content)
            click.echo('')
            click.echo('')

def __do_command(cmd, *params, **kwparams):
    cmd = cmd.replace('-', '_')
    return globals()[cmd](*params, **kwparams)

def _get_dump_files(backupdir, fnfilter=None):
    import humanize
    _files = list(backupdir.glob('*'))

    def _get_ctime(filepath):
        if fnfilter and fnfilter not in filepath.name:
            return False
        try:
            return (backupdir / filepath).stat().st_ctime
        except Exception:
            return 0
    rows = []
    for i, file in enumerate(sorted(filter(lambda x: _get_ctime(x), _files), reverse=True, key=_get_ctime)):
        filepath = backupdir / file
        delta = arrow.get() - arrow.get(filepath.stat().st_mtime)
        rows.append((i + 1, file.name, humanize.naturaltime(delta), humanize.naturalsize(filepath.stat().st_size)))
    return rows

def _dropdb(config, conn):
    if _exists_db(conn):
        if not config.force:
            questions = [inquirer.Text('name', message=f'Database {conn.dbname} will be dropped. Please enter the name to delete it ({conn.shortstr()})')]
            answer = inquirer.prompt(questions)
            if answer['name'] != conn.dbname:
                abort(f'Dropping aborted - you did not answer: {conn.dbname}')
    else:
        click.echo('Database does not exist yet: {}'.format(conn.dbname))
    click.echo('Stopping all services and creating new database')
    _remove_postgres_connections(conn, 'drop database {};'.format(conn.dbname))
    click.echo('Database dropped {}'.format(conn.dbname))

def remove_webassets(conn):
    click.echo('Removing web assets')
    conn = conn.get_psyco_connection()
    cr = conn.cursor()
    urls_to_ignore = ['/website/static/src/scss/options/user_values.custom.web.assets_common.scss', '/website/static/src/scss/options/colors/user_color_palette.custom.web.assets_common.scss', '/website/static/src/scss/options/colors/user_theme_color_palette.custom.web.assets_common.scss', '/website/static/src/scss/options/colors/user_gray_color_palette.scss', '/website/static/src/scss/options/user_values.scss', '/web/static/src/scss/asset_styles_company_report.scss']
    ignore_url_str = ''
    for url in urls_to_ignore:
        ignore_url_str += f" and url != '{url}'"
    queries = [f"delete from ir_attachment where res_model = 'ir.ui.view' and name ilike '%assets_%' {ignore_url_str};", f"delete from ir_attachment where res_model = 'ir.ui.view' and name ilike '%web_editor.summernote%' {ignore_url_str};", f"delete from ir_attachment where res_model = 'ir.ui.view' and name ilike '%.less%' {ignore_url_str};", f"delete from ir_attachment where res_model = 'ir.ui.view' and name ilike '%.scss%' {ignore_url_str};", f"delete from ir_attachment where name ilike '/web/%web%asset%' {ignore_url_str}", f"delete from ir_attachment where name ilike 'import_bootstrap.less' {ignore_url_str}", f"delete from ir_attachment where name ilike '%.less' {ignore_url_str}", f"delete from ir_attachment where name ilike '%.scss' {ignore_url_str}", f"delete from ir_attachment where name ilike 'web_icon_data' {ignore_url_str}", f"delete from ir_attachment where name ilike 'web_editor.summernote.%' {ignore_url_str}", f"delete from ir_attachment where name ilike 'web.assets_backend_prod_only.js'"]
    try:
        for query in queries:
            try:
                click.secho(query, fg='grey')
                cr.execute(query)
                conn.commit()
            except:
                continue
    finally:
        cr.close()
        conn.close()
    click.secho('A restart is usually required, when deleting web assets.', fg='green')

def get_dockercompose():
    from . import files
    import yaml
    content = __read_file(files['docker_compose'])
    compose = yaml.safe_load(content)
    return compose

def get_volume_names():
    from . import project_name
    vols = get_dockercompose()['volumes'].keys()
    return [f'{project_name}_{x}' for x in vols]

def __running_as_root_or_sudo():
    output = subprocess.check_output(['/usr/bin/id', '-u']).strip().decode('utf-8')
    return output == '0'

def __replace_all_envs_in_str(content, env):
    """
    Docker does not allow to replace volume names or
    service names, so we do it by hand
    """
    all_params = re.findall('\\$\\{[^\\}]*?\\}', content)
    for param in all_params:
        name = param
        name = name.replace('${', '')
        name = name.replace('}', '')
        if name in env.keys():
            content = content.replace(param, env[name])
    return content

def __remove_tree(dir, retry=3, interval=2):
    if retry == 0:
        retry = 1
        interval = 0
    E = None
    for i in range(retry):
        try:
            shutil.rmtree(dir)
        except Exception as e:
            E = e
            time.sleep(interval)
        else:
            return
    if E:
        raise E

def __hash_odoo_password(pwd):
    from .odoo_config import current_version
    if current_version() in [9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]:
        setpw = CryptContext(schemes=['pbkdf2_sha512', 'md5_crypt'])
        return setpw.encrypt(pwd)
    else:
        raise NotImplementedError()

def abort(msg, nr=1):
    click.secho(msg, fg='red', bold=True)
    sys.exit(nr)

def sync_folder(dir, dest_dir, excludes=None):
    dir = Path(dir)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(exist_ok=True, parents=True)
    if not dir or not dest_dir or len(str(dir)) < 5 or (len(str(dest_dir)) < 5):
        raise Exception('invalid dirs: {} {}'.format(dir, dest_dir))
    if platform.system() in ['Linux', 'Darwin']:
        cmd = ['rsync', str(dir) + '/', str(dest_dir) + '/', '-r', '--delete-after']
        for exclude in excludes or []:
            cmd += ['--exclude={}'.format(exclude)]
        subprocess.check_call(cmd)
    else:
        raise NotImplementedError()

def rsync(src, dest, options='-ar', exclude=None):
    exclude = exclude or ''
    exclude_option = []
    for x in exclude:
        exclude_option += ['--exclude', x]
    subprocess.check_call(['rsync', str(src) + '/', str(dest) + '/', options] + exclude_option)

def copy_dir_contents(dir, dest_dir, exclude=None):
    assert dir.is_dir()
    assert dest_dir.is_dir()
    exclude = exclude or []
    files = list(dir.glob('*'))
    for x in files:
        if exclude:
            if x.name in exclude:
                continue
        dest_path = (dest_dir / x.name).absolute()
        if not x.is_dir():
            shutil.copy(str(x.absolute()), str(dest_path))
        else:
            shutil.copytree(str(x.absolute()), str(dest_path))

def _get_host_ip():
    conn = os.getenv('SSH_CONNECTION', '')
    if conn:
        conn = [x for x in conn.split(' ') if x]
        return conn[2]

def _is_dirty(repo, check_submodule, assert_clean=False):
    from git import Repo
    from git import InvalidGitRepositoryError
    from git import NoSuchPathError

    def raise_error():
        if assert_clean:
            click.secho('Dirty directory - please cleanup: {repo.working_dir}', bold=True, fg='red')
            sys.exit(42)
    if repo.is_dirty() or repo.untracked_files:
        raise_error()
        return True
    if check_submodule:
        try:
            repo.submodules
        except AttributeError:
            pass
        else:
            for submodule in repo.submodules:
                try:
                    sub_repo = Repo(submodule.path)
                except InvalidGitRepositoryError:
                    click.secho(f'Invalid Repo: {submodule}', bold=True, fg='red')
                except NoSuchPathError:
                    click.secho(f'Invalid Repo: {submodule}', bold=True, fg='red')
                else:
                    if _is_dirty(sub_repo, True, assert_clean=assert_clean):
                        raise_error()
                        return True
    return False

def __assure_gitignore(gitignore_file, content):
    p = Path(gitignore_file)
    if not p.exists():
        p.write_text(content + '\n')
        return
    exists = [l for l in gitignore_file.read_text().splitlines() if l.strip() == content]
    if not exists:
        with p.open('a') as f:
            f.write(content)
            f.write('\n')

def __needs_docker(config):
    if not config.use_docker:
        click.secho('Docker needed USE_DOCKER=1', fg='red')
        sys.exit(1)

def exec_file_in_path(filename):

    def _g():
        for p in ['/usr/local/bin', '/usr/bin', '/bin']:
            filepath = Path(p) / filename
            if filepath.exists():
                yield filepath
    try:
        return next(_g())
    except StopIteration:
        raise Exception(f'Could not find in path: {filename}')

def measure_time(method):

    def wrapper(*args, **kwargs):
        started = datetime.now()
        result = method(*args, **kwargs)
        ended = datetime.now()
        duration = (ended - started).total_seconds()
        if os.getenv('WODOO_VERBOSE', '') == '1':
            click.secho(f'Took: {duration} seconds for {method}', fg='yellow')
        return result
    return wrapper

def _extract_python_libname(x):
    regex = re.compile('[\\w\\-\\_]*')
    x = x.replace('-', '_')
    match = re.findall(regex, x)[0]
    return match

def split_hub_url(config):
    """
    Splits hub url into user, password and url and prefix
    user:password@registry.itewimmer.de:443/prefix
    """
    url = config.HUB_URL
    if not url:
        click.secho('No docker registry hub configured.Please set setting HUB_URL in settings file.', fg='yellow')
        return None
    username, password = url.split(':', 1)
    password = password.split('@')[0]
    url = url.split('@')[1]
    url, prefix = url.split('/', 1)
    return {'url': url, 'password': password, 'username': username, 'prefix': prefix}

def execute_script(config, script, message):
    if script.exists():
        click.secho(f'Executing reload script: {script}', fg='green')
        os.system(script)
    elif config.verbose:
        click.secho(f'{message}\n{script}', fg='yellow')

def get_services(config, based_on, yml=None):
    import yaml
    content = yml or yaml.safe_load(config.files['docker_compose'].read_text())

    def collect():
        for service_name, service in content['services'].items():
            merge = service.get('labels', {}).get('compose.merge')
            if merge and based_on in merge or merge == based_on:
                yield service_name
    res = list(set(collect()))
    return res

def search_env_path(executable_file):

    def _search():
        for path in os.getenv('PATH').split(':'):
            yield from Path(path).glob(executable_file)
    res = list(_search())
    if res:
        return res[0]
    raise Exception(f'Not found: {executable_file}')

def download_file_and_move(url, dest):
    file = download_file(url)
    file.rename(dest)

def download_file(url):
    print(f'Downloading {url}')
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return Path(local_filename)

def get_hash(text):
    if isinstance(text, str):
        text = text.encode('utf8')
    return hashlib.sha1(text).hexdigest()

def get_directory_hash(path):
    click.secho(f'Calculating hash for {path}', fg='yellow')
    hex = subprocess.check_output(['dtreetrawl', '-N', '--hash', '-R', path], encoding='utf8').strip().split(' ')[0].strip()
    return hex

def git_diff_files(path, commit1, commit2):
    params = ['git', 'diff', '--name-only']
    if commit1:
        params += [commit1]
    if commit2:
        params += [commit2]
    output = subprocess.check_output(params, encoding='utf8', cwd=path)
    filepaths = list(filter(bool, output.splitlines()))
    return filepaths

def _binary_zip(folder, destpath):
    assert not destpath.exists()
    if not Path(folder).exists():
        raise Exception(f'Could not zip folder: {folder}')
    os.system(f"cd '{folder}' && tar c . | pv | pigz > '{destpath}'")
    if not destpath.exists():
        raise Exception(f'file {destpath} not generated')

@contextmanager
def autocleanpaper(filepath=None, strict=False):
    if strict:
        assert filepath
    else:
        filepath = Path(filepath or tempfile._get_default_tempdir()) / next(tempfile._get_candidate_names())
    try:
        yield filepath
    finally:
        if filepath.exists():
            if filepath.is_dir():
                shutil.rmtree(filepath)
            else:
                filepath.unlink()

def put_appendix_into_file(appendix, input_filepath, output_filepath):
    with autocleanpaper() as tempfile:
        tempfile.write_text(f'{appendix}')
        os.system(f'cat {tempfile} {input_filepath} > {output_filepath}')

def _get_version():
    import inspect
    import os
    from pathlib import Path
    current_dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    version = (current_dir / 'version.txt').read_text().strip()
    return version

def get_filesystem_of_folder(path):
    df = search_env_path('df')
    lines = subprocess.check_output([df, '-T', path], encoding='utf8').strip().splitlines()
    fstype = list(filter(bool, lines[1].replace('\t', ' ').split(' ')))[1]
    return fstype

def get_git_hash(path=None):
    return subprocess.check_output(['git', 'log', '-n', '1', '--format=%H'], cwd=path or os.getcwd(), encoding='utf8').strip()

def is_git_clean(path=None, ignore_files=None):
    ignore_files = ignore_files or []
    path = path or Path(os.getcwd())
    if not (path / '.git').exists():
        return True
    status = subprocess.check_output(['git', 'status', '--porcelain'], encoding='utf8', cwd=path).strip().splitlines()
    status = list(filter(lambda x: x.strip().split(' ', 1)[1] not in ignore_files, status))
    if status:
        click.secho(f'unclean git: {status}')
    return not status

def whoami(id=False):
    if os.getenv('SUDO_USER') and id:
        return int(subprocess.check_output(['/usr/bin/id', '-u', os.environ['SUDO_USER']], encoding='utf8').strip())
    elif os.getenv('SUDO_USER') and (not id):
        return os.getenv('SUDO_USER')
    elif os.getenv('SUDO_UID') and id:
        return int(os.getenv('SUDO_UID'))
    elif os.getenv('SUDO_UID') and (not id):
        return subprocess.check_output(['/usr/bin/id', '-u', '-n', os.environ['SUDO_UID']], encoding='utf8').strip()
    elif id:
        whoami = subprocess.check_output(['/usr/bin/id', '-u'], encoding='utf8').strip()
        return int(whoami)
    whoami = subprocess.check_output(['/usr/bin/whoami'], encoding='utf8').strip()
    return whoami

@contextmanager
def download_file(url):
    local_filename = url.split('/')[-1]
    file = Path(tempfile.mktemp(suffix='.download'))
    file.mkdir(parents=True)
    file = file / local_filename
    del local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    try:
        yield file
    finally:
        if file.exists():
            file.unlink()

def _get_default_project_name(restrict):
    from .exceptions import NoProjectNameException

    def _get_project_name_from_file(path):
        path = Path(path)
        if not path.exists():
            return
        pj = [x for x in path.read_text().split('\n') if 'PROJECT_NAME' in x]
        if pj:
            return pj[0].split('=')[-1].strip()
    if restrict:
        paths = restrict
    else:
        paths = [Path(os.path.expanduser('~/.odoo/settings'))]
    for path in paths:
        pj = _get_project_name_from_file(path)
        if pj:
            return pj
    customs_root = _get_customs_root(Path(os.getcwd()))
    if customs_root:
        root = Path(customs_root)
        if (root / 'MANIFEST').exists():
            return root.name
    raise NoProjectNameException('No default project name could be determined.')

def _search_path(filename):
    filename = Path(filename)
    filename = filename.name
    paths = os.getenv('PATH', '').split(':')
    execparent = Path(sys.executable).parent
    if execparent.name in ['bin', 'sbin']:
        paths = [execparent] + paths
    for path in paths:
        path = Path(path)
        if (path / filename).exists():
            return str(path / filename)

def _get_customs_root(p):
    if p:
        while len(p.parts) > 1:
            if (p / 'MANIFEST').exists():
                return p
            p = p.parent

def _shell_complete_file(ctx, param, incomplete):
    incomplete = os.path.expanduser(incomplete)
    if not incomplete:
        start = Path(os.getcwd())
    else:
        start = Path(incomplete).parent
    parts = list(filter(bool, incomplete.split('/')))
    if Path(incomplete).exists() and Path(incomplete).is_dir():
        start = Path(incomplete)
        filtered = '*'
    else:
        filtered = '*'
        if parts:
            filtered = parts[-1] + '*'
    files = list(start.glob(filtered))
    return sorted(map(str, files))

def ensure_project_name(config):
    if not config.project_name:
        abort('Project name missing.')

def _get_filestore_folder(config):
    return config.dirs['odoo_data_dir'] / 'filestore' / config.dbname

def _write_file(file, content):
    s = ''
    if file.exists():
        s = file.read_text()
    if s != content:
        file.write_text(content)
        return True
    return False

def _make_sure_module_is_installed(ctx, config, modulename, repo_url):
    from .module_tools import DBModules
    from .odoo_config import MANIFEST
    from .odoo_config import current_version
    from .cli import cli, pass_config, Commands
    from gimera.gimera import add as gimera_add
    from gimera.gimera import apply as gimera_apply
    state = DBModules.get_meta_data(modulename)
    if state['state'] == 'installed':
        return
    path = Path('addons_wodoo') / modulename
    if not path.exists():
        ctx.invoke(gimera_add, url=repo_url, path=str(path), branch=str(current_version()), type='integrated')
        ctx.invoke(gimera_apply, repos=str(path))
    manifest = MANIFEST()
    addons_paths = manifest.get('addons_paths', [])
    install = manifest.get('install', [])
    if modulename not in install:
        install += [modulename]
    manifest['install'] = install
    if str(path) not in addons_paths:
        addons_paths += [str(path)]
        manifest['addons_paths'] = addons_paths
    manifest.rewrite()
    Commands.invoke(ctx, 'update', module=[modulename], no_restart=False, no_dangling_check=True, no_update_module_list=False, non_interactive=True)

def bashfind(path, name=None, wholename=None, type=None):
    cmd = ['find']
    if type:
        cmd += ['-type', type]
    if wholename:
        cmd += ['-wholename', wholename]
    if name:
        cmd += ['-name', name]
    files = subprocess.check_output(cmd, cwd=path, encoding='utf8').splitlines()
    return map(lambda x: Path(path) / x, files)

def _update_setting(conn, key, value):
    value = str(value)
    _execute_sql(conn, f"DELETE FROM ir_config_parameter WHERE key = '{key}'; INSERT INTO ir_config_parameter(key, value, create_date, write_date) values('{key}', '{value}', now(), now());")

def _get_setting(conn, key):
    rec = _execute_sql(conn, f"SELECT value FROM ir_config_parameter WHERE key = '{key}'", fetchone=True)
    if rec:
        return rec[0]

@contextmanager
def cwd(path):
    remember = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(remember)

@contextmanager
def atomic_write(file):
    tempfile = file.parent / f'{file.name}.{uuid.uuid4()}'
    yield tempfile
    if file.exists():
        file.unlink()
    tempfile.rename(file)

def bash_find(path, name=None, wholename=None, type=None):
    cmd = ['find']
    if type:
        cmd += ['-type', type]
    if wholename:
        cmd += ['-wholename', wholename]
    if name:
        cmd += ['-name', name]
    files = subprocess.check_output(cmd, cwd=path, encoding='utf8').splitlines()
    return list(map(lambda x: Path(path) / x, files))