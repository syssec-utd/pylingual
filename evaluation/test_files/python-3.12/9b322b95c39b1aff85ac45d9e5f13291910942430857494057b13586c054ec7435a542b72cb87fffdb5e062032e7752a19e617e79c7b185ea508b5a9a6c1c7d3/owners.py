from .base import DoorLoopBase

class DoorLoopOwner(DoorLoopBase):
    endpoint_base = '/owners'

    def list(self, **kwargs):
        """
        List all Owners
        https://api.doorloop.com/reference/get-owners
        """
        response = self.connector.get(f'{self.endpoint_base}', **kwargs)
        return self.validator(response).validate()

    def create(self, data, **kwargs):
        """
        Create an Owner
        https://api.doorloop.com/reference/post-owner
        """
        response = self.connector.post(f'{self.endpoint_base}', data, **kwargs)
        return self.validator(response).validate()

    def retrieve(self, owner_id, **kwargs):
        """
        Retrieve an Owner
        https://api.doorloop.com/reference/get-owner
        """
        response = self.connector.get(f'{self.endpoint_base}/{owner_id}', **kwargs)
        return self.validator(response).validate()

    def update(self, owner_id, data, **kwargs):
        """
        Update an Owner
        https://api.doorloop.com/reference/put-owner
        """
        response = self.connector.put(f'{self.endpoint_base}/{owner_id}', data, **kwargs)
        return self.validator(response).validate()

    def delete(self, owner_id, **kwargs):
        """
        Delete an Owner
        https://api.doorloop.com/reference/delete-owner
        """
        response = self.connector.delete(f'{self.endpoint_base}/{owner_id}', **kwargs)
        return self.validator(response).validate()