from typing import Any, Dict, List, Optional
from deeplabel.exceptions import InvalidIdError
from deeplabel.basemodel import DeeplabelBase, MixinConfig
import deeplabel.label.folders
import deeplabel.label.videos
import deeplabel.label.label_maps
import deeplabel.client
import deeplabel

class _ProjectProgress(MixinConfig):
    total: int
    completed: int

class _ProjectOwner(MixinConfig):
    name: str
    user_id: str

class Project(DeeplabelBase):
    project_id: str
    title: str
    description: Optional[str]
    organization_id: str
    progress: Optional[_ProjectProgress]
    owner: _ProjectOwner

    @classmethod
    def from_search_params(cls, params: Dict[str, Any], client: 'deeplabel.client.BaseClient') -> List['Project']:
        resp = client.get(client.label_url + '/projects', params)
        projects = resp.json()['data']['projects']
        projects = [cls(**project, client=client) for project in projects]
        return projects

    @classmethod
    def from_project_id(cls, project_id: str, client: 'deeplabel.client.BaseClient') -> 'Project':
        projects = cls.from_search_params({'projectId': project_id}, client)
        if not projects:
            raise InvalidIdError(f'No Project found with projectId: {project_id}')
        return projects[0]

    @property
    def image_datasets(self):
        return deeplabel.label.folders.RootFolder(project_id=self.project_id, type=deeplabel.label.folders.FolderType.GALLERY, folder_id=None, client=self.client)

    @property
    def video_datasets(self):
        return deeplabel.label.folders.RootFolder(project_id=self.project_id, type=deeplabel.label.folders.FolderType.VIDEO, folder_id=None, client=self.client)

    @property
    def label_map(self) -> List['deeplabel.label.label_maps.LabelMap']:
        return deeplabel.label.label_maps.LabelMap.from_search_params({'projectId': self.project_id}, self.client)