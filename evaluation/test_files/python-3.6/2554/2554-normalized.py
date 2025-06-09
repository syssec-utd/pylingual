def reboot_role_instance(self, service_name, deployment_name, role_instance_name):
    """
        Requests a reboot of a role instance that is running in a deployment.

        service_name:
            Name of the hosted service.
        deployment_name:
            The name of the deployment.
        role_instance_name:
            The name of the role instance.
        """
    _validate_not_none('service_name', service_name)
    _validate_not_none('deployment_name', deployment_name)
    _validate_not_none('role_instance_name', role_instance_name)
    return self._perform_post(self._get_deployment_path_using_name(service_name, deployment_name) + '/roleinstances/' + _str(role_instance_name) + '?comp=reboot', '', as_async=True)