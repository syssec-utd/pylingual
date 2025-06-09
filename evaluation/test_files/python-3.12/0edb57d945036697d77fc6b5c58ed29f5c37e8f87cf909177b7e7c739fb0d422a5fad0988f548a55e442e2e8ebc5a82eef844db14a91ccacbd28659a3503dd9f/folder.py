from typing import List
from lib.core import entities
from lib.core.conditions import Condition
from lib.core.service_types import FolderResponse
from lib.core.serviceproviders import BaseFolderService

class FolderService(BaseFolderService):
    URL_BASE = 'folder'
    URL_LIST = 'folders'
    URL_UPDATE = 'folder/{}'
    URL_GET_BY_NAME = 'folder/getFolderByName'
    URL_DELETE_MULTIPLE = 'image/delete/images'
    URL_ASSIGN_FOLDER = 'folder/editAssignment'

    def get_by_name(self, project: entities.ProjectEntity, name: str):
        params = {'project_id': project.id, 'name': name}
        return self.client.request(self.URL_GET_BY_NAME, 'get', params=params, content_type=FolderResponse)

    def create(self, project: entities.ProjectEntity, folder: entities.FolderEntity):
        data = {'name': folder.name}
        params = {'project_id': project.id}
        return self.client.request(self.URL_BASE, 'post', data=data, params=params, content_type=FolderResponse)

    def list(self, condition: Condition=None):
        return self.client.paginate(url=self.URL_LIST, item_type=entities.FolderEntity, query_params=condition.get_as_params_dict() if condition else None)

    def delete_multiple(self, project: entities.ProjectEntity, folders: List[entities.FolderEntity]):
        params = {'project_id': project.id}
        return self.client.request(self.URL_DELETE_MULTIPLE, 'put', params=params, data={'folder_ids': [i.id for i in folders]})

    def un_assign_all(self, project: entities.ProjectEntity, folder: entities.FolderEntity):
        return self.client.request(self.URL_ASSIGN_FOLDER, 'post', params={'project_id': project.id}, data={'folder_name': folder.name, 'remove_user_ids': ['all']})

    def assign(self, project: entities.ProjectEntity, folder: entities.FolderEntity, users: list):
        return self.client.request(self.URL_ASSIGN_FOLDER, 'post', params={'project_id': project.id}, data={'folder_name': folder.name, 'assign_user_ids': users})

    def update(self, project: entities.ProjectEntity, folder: entities.FolderEntity):
        params = {'project_id': project.id}
        return self.client.request(self.URL_UPDATE.format(folder.id), 'put', data=folder.dict(), params=params)