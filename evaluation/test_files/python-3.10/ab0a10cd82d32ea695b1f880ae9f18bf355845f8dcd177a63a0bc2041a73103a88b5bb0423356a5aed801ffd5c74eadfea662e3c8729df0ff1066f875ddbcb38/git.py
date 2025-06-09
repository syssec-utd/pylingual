import os
import subprocess
from typing import Any, Dict, List
import woodchips
from harvey.config import Config
from harvey.utils.deployments import kill_deployment
from harvey.webhooks import Webhook

class Git:

    @staticmethod
    def update_git_repo(webhook: Dict[str, Any]) -> str:
        """Clone or pull repo using Git depending on if it exists or not."""
        project_path = os.path.join(Config.projects_path, Webhook.repo_full_name(webhook))
        if os.path.exists(project_path):
            output = Git.pull_repo(project_path, webhook)
        else:
            output = Git.clone_repo(project_path, webhook)
        return output

    @staticmethod
    def clone_repo(project_path: str, webhook: Dict[str, Any]) -> str:
        """Clone a repo into the Harvey projects folder."""
        logger = woodchips.get(Config.logger_name)
        decoded_output = ''
        try:
            command = ['git', 'clone', '--depth=1', Webhook.repo_url(webhook), project_path]
            command_output = Git._git_subprocess(command)
            decoded_output = command_output.decode()
            logger.debug(decoded_output)
        except subprocess.TimeoutExpired:
            kill_deployment(message='Harvey timed out during git clone operation.', webhook=webhook)
        except subprocess.CalledProcessError as error:
            final_output = f'Harvey could not clone due to error: {error} {Webhook.repo_full_name(webhook)}.'
            kill_deployment(message=final_output, webhook=webhook, raise_error=True)
        return decoded_output

    @staticmethod
    def pull_repo(project_path: str, webhook: Dict[str, Any], pull_attempt: int=1) -> str:
        """Pull updates for a repo in the Harvey projects folder."""
        logger = woodchips.get(Config.logger_name)
        decoded_output = ''
        try:
            command = ['git', '-C', project_path, 'pull', '--rebase']
            command_output = Git._git_subprocess(command)
            decoded_output = command_output.decode()
            logger.debug(f'{decoded_output}')
        except subprocess.TimeoutExpired:
            kill_deployment(message='Harvey timed out during git pull operation.', webhook=webhook)
        except subprocess.CalledProcessError:
            logger.error(f'Harvey could not pull {Webhook.repo_full_name(webhook)}.')
            logger.info(f'Attempting to stash {Webhook.repo_full_name(webhook)} before pulling again...')
            try:
                command = ['git', '-C', project_path, 'stash']
                command_output = Git._git_subprocess(command)
                decoded_output = command_output.decode()
                logger.debug(f'{decoded_output}')
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                kill_deployment(message='Harvey could not stash local changes!', webhook=webhook, raise_error=True)
            if pull_attempt == 1:
                pull_attempt += 1
                decoded_output = Git.pull_repo(project_path, webhook, pull_attempt)
        return decoded_output

    @staticmethod
    def _git_subprocess(command: List[str]) -> bytes:
        """Runs a git command via subprocess."""
        command_output = subprocess.check_output(command, stdin=None, stderr=None, timeout=Config.operation_timeout)
        return command_output