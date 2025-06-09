import logging
import logging.handlers
import sys
import click
import click_log
import shutil
import datetime
import os
import zipfile
import requests
import io
import tempfile
import platform
from pathlib import Path
import typing as t
import atexit
import subprocess
from .config import xml_overlay
from . import utils, templates, core, VERSION, CORE_COMMIT
from .project import Project
log = logging.getLogger('ptxlogger')
click_log.basic_config(log)
click_log_format = click_log.ColorFormatter()
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(click_log_format)
mh = logging.handlers.MemoryHandler(capacity=1024 * 100, flushLevel=100, target=sh, flushOnClose=False)
mh.setLevel(logging.ERROR)
log.addHandler(mh)
atexit.register(utils.exit_command, mh)
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click_log.simple_verbosity_option(log, help='Sets the severity of log messaging: DEBUG for all, INFO (default) for most, then WARNING, ERROR, and CRITICAL for decreasing verbosity.')
@click.version_option(VERSION, message=VERSION)
@click.option('-t', '--targets', is_flag=True, help='Display list of build/view "targets" available in the project manifest.')
def main(ctx, targets):
    """
    Command line tools for quickly creating, authoring, and building PreTeXt projects.

    PreTeXt Guide for authors and publishers:

    - https://pretextbook.org/documentation.html

    PreTeXt CLI README for developers:

    - https://github.com/PreTeXtBook/pretext-cli/

    Use the `--help` option on any CLI command to learn more, for example,
    `pretext build --help`.
    """
    if utils.project_path() is not None:
        if targets:
            Project().print_target_names()
            return
        fh = logging.FileHandler(utils.project_path() / 'cli.log', mode='w')
        fh.setLevel(logging.DEBUG)
        file_log_format = logging.Formatter('{levelname:<8}: {message}', style='{')
        fh.setFormatter(file_log_format)
        log.addHandler(fh)
        log.info(f'PreTeXt project found in `{utils.project_path()}`.')
        os.chdir(utils.project_path())
        if utils.requirements_version() is None:
            log.warning("Project's CLI version could not be detected from `requirements.txt`.")
            log.warning('Try `pretext init --refresh` to produce a compatible file.')
        elif utils.requirements_version() != VERSION:
            log.warning(f"Using CLI version {VERSION} but project's `requirements.txt`")
            log.warning(f'is configured to use {utils.requirements_version()}. Consider either installing')
            log.warning(f'CLI version {utils.requirements_version()} or changing `requirements.txt` to match {VERSION}.')
        else:
            log.debug(f'CLI version {VERSION} matches requirements.txt {utils.requirements_version()}.')
    else:
        log.info('No existing PreTeXt project found.')
    if ctx.invoked_subcommand is None:
        log.info('Run `pretext --help` for help.')

@main.command(short_help='Use when communicating with PreTeXt support.', context_settings=CONTEXT_SETTINGS)
def support():
    """
    Outputs useful information about your installation needed by
    PreTeXt volunteers when requesting help on the pretext-support
    Google Group.
    """
    log.info('')
    log.info('Please share the following information when posting to the')
    log.info('pretext-support Google Group.')
    log.info('')
    log.info(f'PreTeXt-CLI version: {VERSION}')
    log.info(f'    PyPI link: https://pypi.org/project/pretextbook/{VERSION}/')
    log.info(f'PreTeXt core resources commit: {CORE_COMMIT}')
    log.info(f'Runestone Services version: {core.get_runestone_services_version()}')
    log.info(f'OS: {platform.platform()}')
    log.info(f'Python version: {platform.python_version()}')
    log.info(f'Current working directory: {Path().resolve()}')
    if utils.project_path() is not None:
        log.info(f'PreTeXt project path: {utils.project_path()}')
        log.info('')
        log.info('Contents of project.ptx:')
        log.info('------------------------')
        log.info(utils.project_xml_string())
        log.info('------------------------')
        project = Project()
        project.init_ptxcore()
        for exec_name in project.executables():
            if utils.check_executable(exec_name) is None:
                log.warning(f'Unable to locate the command for <{exec_name}> on your system.')
    else:
        log.info('No project.ptx found.')

@main.command(short_help='Alias for the developer pretext/pretext script.', context_settings={'help_option_names': [], 'ignore_unknown_options': True})
@click.argument('args', nargs=-1)
def devscript(args):
    """
    Aliases the core pretext script.
    """
    PY_CMD = sys.executable
    subprocess.run([PY_CMD, core.resources.path('pretext', 'pretext')] + list(args))

@main.command(short_help='Generates the necessary files for a new PreTeXt project.', context_settings=CONTEXT_SETTINGS)
@click.argument('template', default='book', type=click.Choice(['book', 'article', 'demo', 'hello', 'slideshow'], case_sensitive=False))
@click.option('-d', '--directory', type=click.Path(), default='new-pretext-project', help='Directory to create/use for the project.')
@click.option('-u', '--url-template', type=click.STRING, help='Download a zipped template from its URL.')
def new(template, directory, url_template):
    """
    Generates the necessary files for a new PreTeXt project.
    Supports `pretext new book` (default) and `pretext new article`,
    or generating from URL with `pretext new --url-template [URL]`.
    """
    directory_fullpath = Path(directory).resolve()
    if utils.project_path(directory_fullpath) is not None:
        log.warning(f'A project already exists in `{utils.project_path(directory_fullpath)}`.')
        log.warning('No new project will be generated.')
        return
    log.info(f'Generating new PreTeXt project in `{directory_fullpath}` using `{template}` template.')
    if url_template is not None:
        r = requests.get(url_template)
        archive = zipfile.ZipFile(io.BytesIO(r.content))
    else:
        with templates.resource_path(f'{template}.zip') as template_path:
            archive = zipfile.ZipFile(template_path)
    filenames = [Path(filepath).name for filepath in archive.namelist()]
    project_ptx_index = filenames.index('project.ptx')
    project_ptx_path = Path(archive.namelist()[project_ptx_index])
    project_dir_path = project_ptx_path.parent
    with tempfile.TemporaryDirectory() as tmpdirname:
        for filepath in [filepath for filepath in archive.namelist() if project_dir_path in Path(filepath).parents]:
            archive.extract(filepath, path=tmpdirname)
        tmpsubdirname = Path(tmpdirname) / project_dir_path
        shutil.copytree(tmpsubdirname, directory, dirs_exist_ok=True)
    with open(directory_fullpath / 'requirements.txt', 'w') as f:
        f.write(f'pretext == {VERSION}')
    log.info(f'Success! Open `{directory_fullpath}/source/main.ptx` to edit your document')
    log.info(f'Then try to `pretext build` and `pretext view` from within `{directory_fullpath}`.')

@main.command(short_help='Generates the project manifest for a PreTeXt project in the current directory.', context_settings=CONTEXT_SETTINGS)
@click.option('-r', '--refresh', is_flag=True, help='Refresh initialization of project even if project.ptx exists.')
def init(refresh):
    """
    Generates the project manifest for a PreTeXt project in the current directory. This feature
    is mainly intended for updating existing projects to use this CLI.

    If --refresh is used, files will be generated even if the project has already been initialized.
    Existing files won't be overwritten; a copy of the fresh initialized file will be created
    with a timestamp in its filename for comparison.
    """
    if utils.project_path() is not None and (not refresh):
        log.warning(f'A project already exists in `{utils.project_path()}`.')
        log.warning('Use `pretext init --refresh` to refresh initialization of an existing project.')
        return
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    resource_to_dest = {'project.ptx': 'project.ptx', 'publication.ptx': 'publication/publication.ptx', '.gitignore': '.gitignore', 'devcontainer.json': '.devcontainer/devcontainer.json'}
    for resource in resource_to_dest:
        with templates.resource_path(resource) as resource_path:
            project_resource_path = Path(resource_to_dest.get(resource)).resolve()
            if project_resource_path.exists():
                new_resource_name = project_resource_path.stem + '-' + timestamp + project_resource_path.suffix
                project_resource_path = project_resource_path.parent / new_resource_name
                log.warning(f'You already have a {resource} file; a new default one for comparison has been created as {project_resource_path}.')
            log.info(f'Generated `{project_resource_path}`\n')
            if not project_resource_path.parent.exists():
                project_resource_path.parent.mkdir()
            shutil.copyfile(resource_path, project_resource_path)
    requirements_path = Path('requirements.txt').resolve()
    if requirements_path.exists():
        requirements_path = Path(f'requirements-{timestamp}.txt').resolve()
        log.warning(f"You already have a requirements.txt file at {Path('requirements.txt').resolve()}`.")
        log.warning(f'The one suggested by PreTeXt will be created as {requirements_path} for comparison.')
    with open(requirements_path, 'w') as f:
        f.write(f'pretext == {VERSION}')
    log.info(f'Generated requirements file at {requirements_path}.\n')
    log.info('Success! Open project.ptx to edit your project manifest.')
    log.info('Edit your <target/>s to point to the location of your PreTeXt source files.')
ASSETS = ['ALL', 'webwork', 'latex-image', 'sageplot', 'asymptote', 'interactive', 'youtube', 'codelens', 'datafile']

@main.command(short_help='Build specified target', context_settings=CONTEXT_SETTINGS)
@click.argument('target', required=False)
@click.option('--clean', is_flag=True, help="Destroy output's target directory before build to clean up previously built files")
@click.option('-g', '--generate', is_flag=False, flag_value='ALL', default=None, type=click.Choice(ASSETS, case_sensitive=False), help='Generates assets for target.  -g [asset] will generate the specific assets given.')
@click.option('-x', '--xmlid', type=click.STRING, help='xml:id of element to be generated.')
@click.option('-p', '--project-ptx-override', type=(str, str), multiple=True, help=xml_overlay.USAGE_DESCRIPTION.format('-p'))
def build(target, clean, generate, xmlid: t.Optional[str], project_ptx_override: t.Tuple[str, str]):
    """
    Build [TARGET] according to settings specified by project.ptx.

    If using certain elements (webwork, latex-image, etc.) then
    using `--generate` may be necessary for a successful build. Generated
    assets are cached so they need not be regenerated in subsequent builds unless
    they are changed.

    Certain builds may require installations not included with the CLI, or internet
    access to external servers. Command-line paths
    to non-Python executables may be set in project.ptx. For more details,
    consult the PreTeXt Guide: https://pretextbook.org/documentation.html
    """
    if xmlid:
        project_ptx_override += (('targets.target.xmlid-root', xmlid),)
    overlay = xml_overlay.ShadowXmlDocument()
    for (path, value) in project_ptx_override:
        overlay.upsert_node_or_attribute(path, value)
    target_name = target
    if utils.no_project(task='build'):
        return
    project = Project()
    if len(project_ptx_override) > 0:
        messages = project.apply_overlay(overlay)
        for message in messages:
            log.info('project.ptx overlay ' + message)
    target = project.target(name=target_name)
    if target_name is None:
        log.info(f'Since no build target was supplied, the first target of the project.ptx manifest ({target.name()}) will be built.')
        target_name = target.name()
    if target is None:
        utils.show_target_hints(target_name, project, task='build')
        log.critical('Exiting without completing build.')
        return
    if generate == 'ALL':
        log.info('Generating all assets in default formats.')
        project.generate(target.name())
    elif generate is not None:
        log.warning(f'Generating only {generate} assets.')
        project.generate(target.name(), asset_list=[generate])
    else:
        log.warning('Assets like latex-images will not be regenerated for this build')
        log.warning('(previously generated assets will be used if they exist).')
        log.warning('To generate these assets before building, run `pretext build -g`.')
    project.build(target.name(), clean)

@main.command(short_help='Generate specified assets for specified target', context_settings=CONTEXT_SETTINGS)
@click.argument('assets', default='ALL', type=click.Choice(ASSETS, case_sensitive=False))
@click.option('-t', '--target', type=click.STRING, help='Name of target to generate assets for (if not specified, first target from manifest is used).')
@click.option('-x', '--xmlid', type=click.STRING, help='xml:id of element to be generated.')
@click.option('--all-formats', is_flag=True, default=False, help='Generate all possible asset formats rather than just the defaults for the specified target.')
@click.option('-p', '--project-ptx-override', type=(str, str), multiple=True, help=xml_overlay.USAGE_DESCRIPTION.format('-p'))
def generate(assets: str, target: t.Optional[str], all_formats: bool, xmlid: t.Optional[str], project_ptx_override: t.Tuple[str, str]):
    """
    Generate specified (or all) assets for the default target (first target in "project.ptx"). Asset "generation" is typically
    slower and performed less frequently than "building" a project, but is
    required for many PreTeXt features such as webwork and latex-image.

    Certain assets may require installations not included with the CLI, or internet
    access to external servers. Command-line paths
    to non-Python executables may be set in project.ptx. For more details,
    consult the PreTeXt Guide: https://pretextbook.org/documentation.html
    """
    if utils.no_project(task='generate assets for'):
        return
    overlay = xml_overlay.ShadowXmlDocument()
    for (path, value) in project_ptx_override:
        overlay.upsert_node_or_attribute(path, value)
    project = Project()
    if len(project_ptx_override) > 0:
        messages = project.apply_overlay(overlay)
        for message in messages:
            log.info('project.ptx overlay ' + message)
    target_name = target
    target = project.target(name=target_name)
    if target_name is None:
        log.info(f'Since no target was specified with the -t flag, we will generate assets for the first target in the manifest ({target.name()}).')
    if target is None:
        utils.show_target_hints(target_name, project, task='generating assets for')
        log.critical('Exiting without generating any assets.')
        return
    if all_formats and assets == 'ALL':
        log.info(f'Generating all assets in all asset formats for the target "{target.name()}".')
        project.generate(target.name(), all_formats=True, xmlid=xmlid)
    elif all_formats:
        log.info(f'Generating only {assets} assets in all asset formats for the target "{target.name()}".')
        project.generate(target.name(), asset_list=[assets], all_formats=True, xmlid=xmlid)
    elif assets == 'ALL':
        log.info(f'Generating all assets in default formats for the target "{target.name()}".')
        project.generate(target.name(), xmlid=xmlid)
    else:
        log.info(f'Generating only {assets} assets in default formats for the target "{target.name()}".')
        project.generate(target.name(), asset_list=[assets], xmlid=xmlid)

@main.command(short_help='Preview specified target based on its format.', context_settings=CONTEXT_SETTINGS)
@click.argument('target', required=False)
@click.option('-a', '--access', type=click.Choice(['public', 'private'], case_sensitive=False), default='private', show_default=True, help='\n    If running a local server,\n    choose whether or not to allow other computers on your local network\n    to access your documents using your IP address. (Ignored when used\n    in CoCalc, which works automatically.)\n    ')
@click.option('-p', '--port', type=click.INT, help='\n    If running a local server,\n    choose which port to use.\n    (Ignored when used\n    in CoCalc, which works automatically.)\n    ')
@click.option('-d', '--directory', type=click.Path(), help='\n    Run local server for provided directory (does not require a PreTeXt project)\n    ')
@click.option('-w', '--watch', is_flag=True, help='\n    Run a build before starting server, and then\n    watch the status of source files,\n    automatically rebuilding target when changes\n    are made. Only supports HTML-format targets, and\n    only recommended for smaller projects or small\n    subsets of projects.\n    ')
@click.option('-b', '--build', is_flag=True, help='\n    Run a build before viewing.\n    ')
@click.option('-g', '--generate', is_flag=False, flag_value='ALL', default=None, type=click.Choice(ASSETS, case_sensitive=False), help='Generate all or specific assets before viewing')
@click.option('--no-launch', is_flag=True, help='By default, pretext view tries to launch the default application to view the specified target.  Setting this suppresses this behavior.')
def view(target: str, access: str, port: t.Optional[int], directory: str, watch: bool, build: bool, generate: t.Optional[str], no_launch: bool):
    """
    Starts a local server to preview built PreTeXt documents in your browser.
    TARGET is the name of the <target/> defined in `project.ptx`.
    """
    if directory is not None:
        if utils.cocalc_project_id() is not None:
            try:
                subdir = directory.relative_to(Path.home())
            except ValueError:
                subdir = ''
            log.info('Directory can be previewed at the following link at any time:')
            log.info(f'    https://cocalc.com/{utils.cocalc_project_id()}/raw/{subdir}')
            return
        port = port or 8000
        utils.run_server(Path(directory), access, port, no_launch=no_launch)
        return
    if utils.no_project(task='view the output for'):
        return
    target_name = target
    project = Project()
    target = project.target(name=target_name)
    if target is None:
        utils.show_target_hints(target_name, project, task='view')
        log.critical('Exiting.')
        return
    if utils.cocalc_project_id() is not None:
        try:
            subdir = target.output_dir().relative_to(Path.home())
        except ValueError:
            subdir = ''
        log.info('Built project can be previewed at the following link at any time:')
        log.info(f'    https://cocalc.com/{utils.cocalc_project_id()}/raw/{subdir}')
        return
    port = port or target.port()
    if generate == 'ALL':
        log.info('Generating all assets in default formats.')
        project.generate(target_name)
    elif generate is not None:
        log.warning(f'Generating only {generate} assets.')
        project.generate(target_name, asset_list=[generate])
    if build or watch:
        log.info('Building target.')
        project.build(target_name)
    project.view(target_name, access, port, watch, no_launch)

@main.command(short_help='Deploys Git-managed project to GitHub Pages.', context_settings=CONTEXT_SETTINGS)
@click.argument('target', required=False)
@click.option('-u', '--update_source', is_flag=True, required=False)
def deploy(target, update_source):
    """
    Automatically deploys most recent build of [TARGET] to GitHub Pages,
    making it available to the general public.
    Requires that your project is under Git version control
    properly configured with GitHub and GitHub Pages. Deployed
    files will live in `docs` subdirectory of project.
    """
    if utils.no_project(task='deploy'):
        return
    target_name = target
    project = Project()
    target = project.target(name=target_name)
    if target is None or target.format() != 'html':
        log.critical('Target could not be found in project.ptx manifest.')
        log.critical(f"Possible html targets to deploy are: {project.target_names('html')}")
        log.critical('Exiting without completing task.')
        return
    project.deploy(target_name, update_source)