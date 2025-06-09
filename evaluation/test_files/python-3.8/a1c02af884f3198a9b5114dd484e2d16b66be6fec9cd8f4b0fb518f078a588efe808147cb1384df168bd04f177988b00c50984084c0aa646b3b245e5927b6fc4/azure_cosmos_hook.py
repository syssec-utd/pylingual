"""This module is deprecated. Please use :mod:`airflow.providers.microsoft.azure.hooks.cosmos`."""
import warnings
from airflow.providers.microsoft.azure.hooks.cosmos import AzureCosmosDBHook
warnings.warn('This module is deprecated. Please use `airflow.providers.microsoft.azure.hooks.cosmos`.', DeprecationWarning, stacklevel=2)