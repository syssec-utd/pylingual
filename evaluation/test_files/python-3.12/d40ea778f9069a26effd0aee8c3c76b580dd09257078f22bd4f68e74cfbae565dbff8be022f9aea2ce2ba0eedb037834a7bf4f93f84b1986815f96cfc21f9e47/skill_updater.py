from mycroft.api import DeviceApi, is_paired
from mycroft.util.log import LOG
from selene_api.settings import SeleneSkillsManifest
from ovos_config import Configuration
from mycroft.deprecated.skills.skill_updater import SkillUpdater

class SeleneSkillManifestUploader:
    """Class facilitating skill manifest upload."""

    def __init__(self):
        super().__init__()
        self.api = DeviceApi()
        self.config = Configuration()
        self.skill_manifest = SeleneSkillsManifest(self.api)
        self.post_manifest(True)

    @property
    def installed_skills_file_path(self):
        """Property representing the path of the installed skills file."""
        return self.skill_manifest.path

    def post_manifest(self, reload_skills_manifest=False):
        """Post the manifest of the device's skills to the backend."""
        upload_allowed = self.config['skills'].get('upload_skill_manifest')
        if upload_allowed and is_paired():
            if reload_skills_manifest:
                self.skill_manifest.clear()
                self.skill_manifest.scan_skills()
            try:
                self.api.upload_skills_data(self.skill_manifest)
            except Exception:
                LOG.error('Could not upload skill manifest')