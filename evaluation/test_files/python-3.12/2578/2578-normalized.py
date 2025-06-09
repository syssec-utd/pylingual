def delete_role(self, service_name, deployment_name, role_name, complete=False):
    """
        Deletes the specified virtual machine.

        service_name:
            The name of the service.
        deployment_name:
            The name of the deployment.
        role_name:
            The name of the role.
        complete:
            True if all OS/data disks and the source blobs for the disks should
            also be deleted from storage.
        """
    _validate_not_none('service_name', service_name)
    _validate_not_none('deployment_name', deployment_name)
    _validate_not_none('role_name', role_name)
    path = self._get_role_path(service_name, deployment_name, role_name)
    if complete == True:
        path = path + '?comp=media'
    return self._perform_delete(path, as_async=True)