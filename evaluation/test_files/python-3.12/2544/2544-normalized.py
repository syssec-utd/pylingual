def get_deployment_by_slot(self, service_name, deployment_slot):
    """
        Returns configuration information, status, and system properties for
        a deployment.

        service_name:
            Name of the hosted service.
        deployment_slot:
            The environment to which the hosted service is deployed. Valid
            values are: staging, production
        """
    _validate_not_none('service_name', service_name)
    _validate_not_none('deployment_slot', deployment_slot)
    return self._perform_get(self._get_deployment_path_using_slot(service_name, deployment_slot), Deployment)