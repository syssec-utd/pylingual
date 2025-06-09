from codecs import ignore_errors
import arrow
import time
import sys
import uuid
from .tools import abort
import sys
import docker
import json
import importlib.util
from retrying import retry
import traceback
from threading import Thread
import subprocess
import shutil
from datetime import datetime
import inquirer
import os
import click
from pathlib import Path
from .tools import put_appendix_into_file
from .tools import _dropdb
from .tools import remove_webassets
from .tools import __dc
from .tools import _execute_sql
from .tools import __rename_db_drop_target
from .tools import _remove_postgres_connections
from .tools import _get_dump_files
from .tools import _binary_zip
from .tools import autocleanpaper
from .tools import _shell_complete_file
from .cli import cli, pass_config, Commands
from .lib_clickhelpers import AliasedGroup
from .tools import ensure_project_name
from .tools import _get_filestore_folder
from .tools import __try_to_set_owner
import inspect
import os
from pathlib import Path
current_dir = Path(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
try:
    import tabulate
except ImportError:
    click.echo('Failed to import python package: tabulate')

@cli.group(cls=AliasedGroup)
@pass_config
def backup(config):
    pass

@cli.group(cls=AliasedGroup)
@pass_config
def restore(config):
    pass

@backup.command(name='all')
@click.argument('filename', required=False)
@pass_config
@click.pass_context
def backup_all(ctx, config, filename):
    """
    Runs backup-db and backup-files in odoo-sh format.
    """
    ensure_project_name(config)
    config.force = True
    filename = Path(filename or config.dbname + arrow.get().strftime('%Y%m%d %H%M') + '.zip')
    if len(filename.parts) == 1:
        filename = Path(config.dumps_path) / filename
    with autocleanpaper(Path(filename.parent) / str(uuid.uuid4())) as tmppath:
        tmppath.mkdir(exist_ok=True, parents=True)
        subprocess.check_output(['chown', str(config.owner_uid), tmppath])
        filepath_db = ctx.invoke(backup_db, filename=tmppath / 'dump.sql', dumptype='plain')
        with autocleanpaper(tmppath / (filename.name + '.zip'), strict=True) as tmpfile:
            folder = _get_filestore_folder(config)
            with autocleanpaper() as fake_filestore:
                symlink_file = fake_filestore / 'filestore'
                symlink_file.parent.mkdir(exist_ok=True, parents=True)
                os.symlink(folder, symlink_file)
                with autocleanpaper(folder / 'zipped.zip', strict=True) as folderzip:
                    subprocess.check_call(['zip', '-r', folderzip, 'filestore'], cwd=fake_filestore)
                    shutil.move(folderzip, tmpfile)
            subprocess.check_call(['zip', '-u', tmpfile, filepath_db.relative_to(tmppath)], cwd=tmppath)
            shutil.move(tmpfile, filename)
    __try_to_set_owner(int(config.owner_uid), filename, verbose=True)
    click.secho(f'Created dump-file {filename}', fg='green')

@backup.command(name='odoo-db')
@pass_config
@click.pass_context
@click.argument('filename', required=False, default='')
@click.option('--dbname', required=False)
@click.option('-T', '--exclude', multiple=True)
@click.option('--column-inserts', is_flag=True, help='Makes restore slow but compatible with other databases')
@click.option('--dumptype', type=click.Choice(['custom', 'plain', 'directory', 'wodoobin']), default='custom')
@click.option('--pigz', is_flag=True)
@click.option('-Z', '--compression', default=5)
@click.option('-j', '--worker', default=1)
def backup_db(ctx, config, filename, dbname, dumptype, column_inserts, exclude, pigz, compression, worker):
    filename = Path(filename or f'{config.project_name}.{config.dbname}.odoo' + '.dump.gz')
    if len(filename.parts) == 1:
        filename = Path(config.dumps_path) / filename
    if dumptype == 'wodoobin':
        _backup_wodoobin(ctx, config, filename)
    else:
        _backup_pgdump(config, filename, dbname or config.DBNAME, config.DB_HOST, config.DB_PORT, config.DB_USER, config.DB_PWD, dumptype, compression, worker, column_inserts, pigz, exclude)
    return filename

@backup.command(name='files')
@click.argument('filename', required=False, default='')
@pass_config
def backup_files(config, filename):
    filepath = Path(filename or f'{config.project_name}.files.tar.gz')
    if len(filepath.parts) == 1:
        filepath = Path(config.dumps_path) / filepath
    if filepath.exists():
        __do_restore_files(config, filepath)
    files_dir = _get_filestore_folder(config)
    if not files_dir.exists():
        return
    subprocess.check_call(['tar', 'cfz', filepath, '.'], cwd=files_dir)
    __apply_dump_permissions(filepath)
    click.secho(f'Backup files done to {filepath}', fg='green')
    return filepath

def __get_default_backup_filename(config):
    return datetime.now().strftime(f'{config.project_name}.odoo.%Y%m%d%H%M%S.dump.gz')

@restore.command('show-dump-type')
@click.argument('filename')
@pass_config
def get_dump_type(config, filename):
    dump_type = _add_cronjob_scripts(config)['postgres'].__get_dump_type(filename)
    click.echo(dump_type)

@restore.command(name='list')
@pass_config
def list_dumps(config):
    rows = _get_dump_files()
    click.echo(tabulate(rows, ['Nr', 'Filename', 'Age', 'Size']))

@restore.command(name='files')
@click.argument('filename', required=True)
@pass_config
def restore_files(config, filename):
    __do_restore_files(config, filename)

def _get_postgres_version(conn):
    version = _execute_sql(conn, 'select version()', fetchone=True)[0]
    version = version.split('(')[0].split(' ')[1]
    version = version.strip()
    click.secho(f'Identified version {version}', fg='green')
    return version

def _restore_wodoo_bin(ctx, config, filepath, verify):
    if not config.run_postgres:
        abort('WODOO-BIN files may only be restored if RUN_POSTGRES=1')
    click.secho(f'Unzipping {filepath}...', fg='yellow')
    with open(filepath, 'rb') as file:
        content = file.read(1024)
        count_lineendings = 0
        cutoff = 0
        for i in range(len(content)):
            cutoff += 1
            if content[i] == ord(b'\n'):
                count_lineendings += 1
            if count_lineendings == 2:
                break
    if verify:
        click.secho(f'Verifying version postgres', fg='yellow')
        Commands.invoke(ctx, 'up', daemon=True, machines=['postgres'])
        postgres_version = content.decode('utf-8', errors='ignore').split('\n')[1].strip()
        conn = config.get_odoo_conn()
        version = _get_postgres_version(conn)
        if version != postgres_version:
            abort(f'Version mismatch: {version} != {postgres_version}')
        click.secho(f'Versions match', fg='green')
    assert config.run_postgres
    Commands.invoke(ctx, 'down')
    volume = json.loads(subprocess.check_output(['docker', 'volume', 'inspect', f'{config.PROJECT_NAME}_odoo_postgres_volume'], encoding='utf-8'))
    mountpoint = volume[0]['Mountpoint']
    click.secho(f'Identified mountpoint {mountpoint}', fg='yellow')
    with autocleanpaper() as scriptfile:
        scriptfile.write_text(f"#!/bin/bash\nset -e\nrm -Rf '{mountpoint}'\nmkdir '{mountpoint}'\ncd '{mountpoint}'\ntail '{filepath}' -c +{cutoff + 1} | pigz -dc | tar x\n")
        for mode in ['', 'sudo']:
            try:
                subprocess.check_call(list(filter(bool, [mode, '/bin/bash', scriptfile])))
            except Exception:
                if mode:
                    raise
                click.secho('Retrying to restore the files in sudo mode - ignore previous errors please', fg='yellow')
            else:
                break
    Commands.invoke(ctx, 'up', machines=['postgres'], daemon=True)

def _odoo_sh(ctx, config, filename, params):
    with autocleanpaper() as tempfolder:
        filename = Path(filename).absolute()
        tempfolder.mkdir(exist_ok=True, parents=True)
        was_dir = os.getcwd()
        try:
            os.chdir(tempfolder)
            if not filename.exists():
                abort(f'File does not exist: {tempfolder}')
            subprocess.check_call(['unzip', filename])
            sqlfile = tempfolder / 'dump.sql'
            filestore = tempfolder / 'filestore'
            if filestore.exists():
                filestore_dest = _get_filestore_destination(config)
                click.secho(f'Transferring files to {filestore_dest}')
                subprocess.check_call(['rsync', str(filestore) + '/', str(filestore_dest) + '/', '-ar'])
                subprocess.check_call(['chown', str(config.owner_uid), filestore_dest, '-R'])
            if sqlfile.exists():
                click.secho(f'Restoring db {sqlfile}')
                os.chdir(was_dir)
                params['no_remove_webassets'] = True
                Commands.invoke(ctx, 'restore_db', filename=sqlfile, **params)
        finally:
            os.chdir(was_dir)

def _after_restore(ctx, conn, config, no_dev_scripts, no_remove_webassets):
    from .lib_turnintodev import __turn_into_devdb
    if config.devmode and (not no_dev_scripts):
        __turn_into_devdb(ctx, config, conn)
        if not no_remove_webassets:
            remove_webassets(conn)

@restore.command(name='odoo-db')
@click.argument('filename', required=False, default='', shell_complete=_shell_complete_file)
@click.option('--no-dev-scripts', default=False, is_flag=True)
@click.option('--no-remove-webassets', default=False, is_flag=True)
@click.option('-j', '--workers', default=5)
@click.option('--verify', default=False, is_flag=True, help='Wodoo-bin: checks postgres version')
@click.option('-X', '--exclude-tables', multiple=True, help='Exclude tables from restore like --exclude=mail_message')
@click.option('-v', '--verbose', is_flag=True)
@click.option('--ignore-errors', is_flag=True, help='Example if some extensions are missing (replication)')
@pass_config
@click.pass_context
def restore_db(ctx, config, filename, no_dev_scripts, no_remove_webassets, verify, workers, exclude_tables, verbose, ignore_errors):
    if not filename:
        filename = _inquirer_dump_file(config, 'Choose filename to restore', config.dbname)
    if not filename:
        return
    if not config.dbname:
        raise Exception('somehow dbname is missing')
    dumps_path = config.dumps_path
    BACKUPDIR = Path(dumps_path)
    filename_absolute = (BACKUPDIR / filename).absolute()
    del filename
    if not config.force:
        __restore_check(filename_absolute, config)
    params = {'no_dev_scripts': no_dev_scripts, 'no_remove_webassets': no_remove_webassets, 'verify': verify, 'workers': workers, 'exclude_tables': exclude_tables, 'verbose': verbose, 'ignore_errors': ignore_errors}
    dump_type = _add_cronjob_scripts(config)['postgres'].__get_dump_type(filename_absolute)
    if dump_type == 'odoosh':
        _odoo_sh(ctx, config, filename=filename_absolute, params=params)
        return
    if len(Path(filename_absolute).parts) > 1:
        dumps_path = Path(filename_absolute).parent
        filename = Path(filename_absolute).name
    if dump_type.startswith('dump_all'):
        with autocleanpaper() as tmpdir:
            params['no_remove_webassets'] = True
            with _add_cronjob_scripts(config)['postgres'].extract_dumps_all(tmpdir, filename_absolute) as (dbfile, files_file):
                ctx.invoke(restore_files, filename=files_file)
                ctx.invoke(restore_db, filename=dbfile, **params)
                return
    if dump_type.startswith('wodoo_bin'):
        if not config.run_postgres:
            abort('Requires RUN_POSTGRES=1')
        _restore_wodoo_bin(ctx, config, filename_absolute, verify)
        conn = config.get_odoo_conn()
        _after_restore(ctx, conn, config, no_dev_scripts, no_remove_webassets)
    else:
        _restore_dump(ctx, config, filename, dumps_path, **params)
    if config.run_postgres:
        __dc(config, ['up', '-d', 'postgres'])
        Commands.invoke(ctx, 'wait_for_container_postgres')
        if config.devmode:
            Commands.invoke(ctx, 'pghba_conf_wide_open')

def _restore_dump(ctx, config, filename, dumps_path, no_dev_scripts, no_remove_webassets, workers, exclude_tables, verbose, verify, ignore_errors):
    DBNAME_RESTORING = config.dbname + '_restoring'
    if config.run_postgres:
        postgres_name = f'{config.PROJECT_NAME}_run_postgres'
        client = docker.from_env()
        for container in client.containers.list(filters={'name': f'{postgres_name}'}):
            container.kill()
            container.remove()
        try:
            Commands.invoke(ctx, 'down')
        except Exception as ex:
            pass
        Commands.invoke(ctx, 'up', machines=['postgres'], daemon=True)
    Commands.invoke(ctx, 'wait_for_container_postgres', missing_ok=True)
    conn = config.get_odoo_conn()
    dest_db = conn.dbname
    conn = conn.clone(dbname=DBNAME_RESTORING)
    with config.forced() as config:
        _dropdb(config, conn)
    _execute_sql(conn.clone(dbname='postgres'), f'create database {DBNAME_RESTORING} ;', notransaction=True)
    effective_host_name = config.DB_HOST
    if config.devmode and (not no_dev_scripts):
        click.echo('Option devmode is set, so cleanup-scripts are run afterwards')
    try:
        if config.use_docker:
            if config.run_postgres:
                __dc(config, ['kill', 'postgres'])
                __dc(config, ['run', '-d', '--name', f'{postgres_name}', '--rm', '--service-ports', '-v', f'{dumps_path}:/host/dumps2', 'postgres'])
                Commands.invoke(ctx, 'wait_for_container_postgres', missing_ok=True)
                effective_host_name = postgres_name
            cmd = ['run', '--rm', '--entrypoint', 'python3 /usr/local/bin/postgres.py']
            parent_path_in_container = '/host/dumps2'
            cmd += ['-v', f'{dumps_path}:{parent_path_in_container}']
            cmd += ['cronjobshell', 'restore', DBNAME_RESTORING, effective_host_name, config.DB_PORT, config.DB_USER, config.DB_PWD, f'{parent_path_in_container}/{filename}', '-j', str(workers)]
            if ignore_errors:
                cmd += ['--ignore-errors']
            if exclude_tables:
                cmd += ['--exclude-tables', ','.join(exclude_tables)]
            if verbose:
                cmd += ['--verbose']
            __dc(config, cmd)
        else:
            _add_cronjob_scripts(config)['postgres']._restore(DBNAME_RESTORING, effective_host_name, config.DB_PORT, config.DB_USER, config.DB_PWD, Path(config.dumps_path) / filename)
        _after_restore(ctx, conn, config, no_dev_scripts, no_remove_webassets)
        __rename_db_drop_target(conn.clone(dbname='postgres'), DBNAME_RESTORING, config.dbname)
        _remove_postgres_connections(conn.clone(dbname=dest_db))
    finally:
        if config.run_postgres:
            subprocess.check_output(['docker', 'stop', postgres_name])
            try:
                subprocess.check_output(['docker', 'kill', postgres_name])
            except subprocess.CalledProcessError:
                pass
            subprocess.check_output(['docker', 'rm', '-f', postgres_name])

def _add_cronjob_scripts(config):
    """
    Adds scripts from images/cronjobs/bin to sys path to be executed.
    """
    spec = importlib.util.spec_from_file_location('bin', config.dirs['images'] / 'cronjobs' / 'bin' / 'postgres.py')
    postgres = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(postgres)
    return {'postgres': postgres}

def _inquirer_dump_file(config, message, filter):
    BACKUPDIR = Path(config.dumps_path)
    __files = _get_dump_files(BACKUPDIR)
    filename = inquirer.prompt([inquirer.List('filename', message, choices=__files)])
    if filename:
        filename = filename['filename'][1]
        return filename

def _get_filestore_destination(config):
    files_dir = config.dirs['odoo_data_dir'] / 'filestore' / config.dbname
    files_dir.mkdir(exist_ok=True, parents=True)
    return files_dir

def __do_restore_files(config, filepath):
    filepath = Path(filepath)
    if len(filepath.parts) == 1:
        filepath = Path(config.dumps_path) / filepath
    files_dir = _get_filestore_destination(config)
    subprocess.check_call(['tar', 'xzf', filepath], cwd=files_dir)
    click.secho(f'Files restored from {filepath} to {files_dir}', fg='green')

def __restore_check(filepath, config):
    pass

def __apply_dump_permissions(filepath):

    def change(cmd, id):
        subprocess.check_call(['sudo', cmd, id, filepath])
    for x in [('DUMP_UID', 'chown'), ('DUMP_GID', 'chgrp')]:
        id = os.getenv(x[0])
        if id:
            change(x[1], id)

def _backup_wodoobin(ctx, config, filename):
    if not config.run_postgres:
        abort('Binary ZIP requires own postgres container. DB is also stopped for that.')
    conn = config.get_odoo_conn()
    version = None
    version = _get_postgres_version(conn)
    Commands.invoke(ctx, 'stop', machines=['postgres'])
    path = json.loads(subprocess.check_output(['docker', 'volume', 'inspect', f'{config.PROJECT_NAME}_odoo_postgres_volume']))[0]['Mountpoint']
    with autocleanpaper() as tempfile_zip:
        _binary_zip(path, tempfile_zip)
        put_appendix_into_file(f'WODOO_BIN\n{version}\n', tempfile_zip, filename)
    Commands.invoke(ctx, 'up', daemon=True, machines=['postgres'])

def _backup_pgdump(config, filename, dbname, db_host, db_port, db_user, db_pwd, dumptype, compression, worker, column_inserts, pigz, exclude):
    click.secho(f'Backup file will be stored there: {filename.parent}')
    cmd = ['run', '--rm', '--entrypoint', 'python3 /usr/local/bin/postgres.py', '-v', f'{filename.parent}:/host/dumps2', 'cronjobshell', 'backup', dbname, db_host, db_port, db_user, db_pwd, '/host/dumps2/' + filename.name, '--dumptype', dumptype, '--compression', str(compression), '-j', str(worker)]
    for exclude in exclude:
        cmd += ['--exclude', exclude]
    if column_inserts:
        cmd += ['--column-inserts']
    if pigz:
        cmd += ['--pigz']
    res = __dc(config, cmd)
    if res:
        raise Exception('Backup failed!')
Commands.register(backup_db)
Commands.register(restore_db)