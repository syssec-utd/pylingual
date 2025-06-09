def get_azure_cli_credentials(resource=None, with_tenant=False):
    """Return Credentials and default SubscriptionID of current loaded profile of the CLI.

    Credentials will be the "az login" command:
    https://docs.microsoft.com/cli/azure/authenticate-azure-cli

    Default subscription ID is either the only one you have, or you can define it:
    https://docs.microsoft.com/cli/azure/manage-azure-subscriptions-azure-cli

    .. versionadded:: 1.1.6

    :param str resource: The alternative resource for credentials if not ARM (GraphRBac, etc.)
    :param bool with_tenant: If True, return a three-tuple with last as tenant ID
    :return: tuple of Credentials and SubscriptionID (and tenant ID if with_tenant)
    :rtype: tuple
    """
    profile = get_cli_profile()
    (cred, subscription_id, tenant_id) = profile.get_login_credentials(resource=resource)
    if with_tenant:
        return (cred, subscription_id, tenant_id)
    else:
        return (cred, subscription_id)