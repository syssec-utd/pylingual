"""
Helper functions for working with Git repositories
"""
from typing import List
import os
import re
import subprocess
from shlex import quote

def get_output_of_command(command: List[str], description: str) -> str:
    """
    subprocess.check_output wrapper that returns string output and raises detailed
    exceptions on error.

    Parameters
    ----------
    command:     list of strings creating a full command
    description: meaningful message for error logging

    Returns
    -------
    stripped output string if command was successful

    """
    try:
        return subprocess.check_output(command).decode().strip()
    except KeyboardInterrupt:
        raise
    except subprocess.CalledProcessError as e:
        raise Exception(f"Couldn't call {description} by calling '{' '.join(command)}', {e}") from e
    except Exception as e:
        raise Exception(f"Couldn't process {description} through calling '{' '.join(command)}', {e}") from e

def get_relative_script_path_from_git_root(script_name: str) -> str:
    """
    If we're in a subdirectory, get the relative path from the git root
    to the current directory, and append the script path.
    For example, the relative path to this script (from git root) is:
        cpg-utils/git.py

    Parameters
    ----------
    script_name

    Returns
    -------
    fully qualified script path from repo root
    """
    base = get_relative_path_from_git_root()
    return os.path.join(base, script_name)

def get_relative_path_from_git_root() -> str:
    """
    If we're in a subdirectory, get the relative path from the git root
    to the current directory. Relpath returns "." if cwd is a git root.
    """
    root = get_git_repo_root()
    return os.path.relpath(os.getcwd(), root)

def get_git_default_remote() -> str:
    """
    Returns the git remote of 'origin',
    e.g. https://github.com/populationgenomics/cpg-utils

    Returns
    -------

    """
    command = ['git', 'remote', 'get-url', 'origin']
    return get_output_of_command(command, 'get Git remote of origin')

def get_git_repo_root() -> str:
    """
    Returns the git repository directory root,
    e.g. /Users/foo/repos/cpg-utils

    Returns
    -------

    """
    command = ['git', 'rev-parse', '--show-toplevel']
    repo_root = get_output_of_command(command, 'get Git repo directory')
    return repo_root

def get_git_commit_ref_of_current_repository() -> str:
    """
    Returns the commit SHA at the current HEAD

    Returns
    -------

    """
    command = ['git', 'rev-parse', 'HEAD']
    return get_output_of_command(command, 'get latest Git commit')

def get_repo_name_from_current_directory() -> str:
    """
    Gets the repo name from the default remote

    Returns
    -------

    """
    return get_repo_name_from_remote(get_git_default_remote())

def get_organisation_name_from_current_directory() -> str:
    """
    Gets the organisation name from the default remote
    Returns
    -------

    """
    return get_organisation_name_from_remote(get_git_default_remote())

def get_organisation_name_from_remote(remote_name: str) -> str:
    """
    Takes the GitHub repo path and obtains the source organisation
    based on its remote URL e.g.:
    >>> get_repo_name_from_remote(        'git@github.com:populationgenomics/cpg-utils.git'    )
    'populationgenomics'
    >>> get_repo_name_from_remote(        'https://github.com/populationgenomics/cpg-utils.git'    )
    'populationgenomics'

    Parameters
    ----------
    remote_name

    Returns
    -------
    the organisation name
    """
    organisation = None
    try:
        if remote_name.startswith('http'):
            match = re.match('http[s]?:\\/\\/[A-z0-9\\.]+?\\/(?P<org>.+?)\\/.+$', remote_name)
            if match:
                organisation = match.group('org')
        elif remote_name.startswith('git@'):
            match = re.match('git@[A-z0-9\\.]+?:(?P<org>.+?)\\/.+$', remote_name)
            if match:
                organisation = match.group('org')
    except AttributeError as ae:
        raise Exception(f'Unsupported remote format: "{remote_name}"') from ae
    if organisation is None:
        raise Exception(f'Unsupported remote format: "{remote_name}"')
    return organisation

def get_repo_name_from_remote(remote_name: str) -> str:
    """
    Get the name of a GitHub repo from a supported organization
    based on its remote URL e.g.:
    >>> get_repo_name_from_remote(        'git@github.com:populationgenomics/cpg-utils.git'    )
    'cpg-utils'
    >>> get_repo_name_from_remote(        'https://github.com/populationgenomics/cpg-utils.git'    )
    'cpg-utils'

    removed check for the authorised organisation(s) here - we receive
    a full repository path, so we trust users will not attempt to run
    potentially harmful code
    """
    repo = None
    try:
        if remote_name.startswith('http'):
            match = re.match('http[s]?:\\/\\/[A-z0-9\\.]+?\\/.+?\\/(?P<repo>.+)$', remote_name)
            if match:
                repo = match.group('repo')
        elif remote_name.startswith('git@'):
            match = re.match('git@[A-z0-9\\.]+?:.+?\\/(?P<repo>.+)$', remote_name)
            if match:
                repo = match.group('repo')
    except AttributeError as ae:
        raise Exception(f'Unsupported remote format: "{remote_name}"') from ae
    if repo is None:
        raise Exception(f'Unsupported remote format: "{remote_name}"')
    if repo.endswith('.git'):
        repo = repo[:-4]
    return repo

def check_if_commit_is_on_remote(commit: str) -> bool:
    """
    Returns 'True' if the commit is available on a remote branch.
    This relies on the current environment to be up-to-date.
    It asks if the local environment knows a remote branch with the commit.

    Parameters
    ----------
    commit

    Returns
    -------

    """
    command = ['git', 'branch', '-r', '--contains', commit]
    try:
        ret = subprocess.check_output(command)
        return bool(ret)
    except subprocess.CalledProcessError:
        return False

def prepare_git_job(job, organisation: str, repo_name: str, commit: str, is_test: bool=True, print_all_statements: bool=True):
    """
    Takes a hail batch job, and:
        * Clones the repository
            * if access_level != "test": check the desired commit is on 'main'
        * Check out the specific commit

    Parameters
    ----------
    job                     - A hail BashJob
    organisation            - The GitHub individual or organisation
    repo_name               - The repository name to check out
    commit                  - The commit hash to check out
    is_test                 - CPG specific: only Main commits can run on Main data
    print_all_statements    - logging toggle

    Returns
    -------
    No return required
    """
    if print_all_statements:
        job.command('set -x')
    job.command(f'git clone --recurse-submodules https://github.com/{quote(organisation)}/{quote(repo_name)}.git')
    job.command(f'cd {quote(repo_name)}')
    if not is_test:
        job.command('git checkout main')
        job.command(f'git merge-base --is-ancestor {quote(commit)} HEAD || {{ echo "error: commit not merged into main branch"; exit 1; }}')
    job.command(f'git checkout {quote(commit)}')
    job.command(f'git submodule update')