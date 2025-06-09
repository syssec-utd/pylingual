from typing import Optional
from reconcile.saas_auto_promotions_manager.utils.deployment_state import DeploymentInfo, DeploymentState
from reconcile.saas_auto_promotions_manager.utils.vcs import VCS
from reconcile.utils.secret_reader import HasSecret

class Publisher:

    def __init__(self, ref: str, repo_url: str, auth_code: Optional[HasSecret]):
        self._ref = ref
        self._repo_url = repo_url
        self._auth_code = auth_code
        self.channels: set[str] = set()
        self.commit_sha: str = ''
        self.deployment_info_by_channel: dict[str, Optional[DeploymentInfo]] = {}

    def fetch_commit_shas_and_deployment_info(self, vcs: VCS, deployment_state: DeploymentState) -> None:
        self.commit_sha = vcs.get_commit_sha(auth_code=self._auth_code, ref=self._ref, repo_url=self._repo_url)
        for channel in self.channels:
            self.deployment_info_by_channel[channel] = None
            deployment_info = deployment_state.get_deployment_info(sha=self.commit_sha, channel=channel)
            self.deployment_info_by_channel[channel] = deployment_info