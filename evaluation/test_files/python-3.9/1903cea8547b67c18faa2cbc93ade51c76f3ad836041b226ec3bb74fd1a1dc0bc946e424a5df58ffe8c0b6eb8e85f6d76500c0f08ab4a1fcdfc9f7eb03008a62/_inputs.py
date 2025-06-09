import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *
__all__ = ['AutoStorageBasePropertiesArgs', 'KeyVaultReferenceArgs']

@pulumi.input_type
class AutoStorageBasePropertiesArgs:

    def __init__(__self__, *, storage_account_id: pulumi.Input[str]):
        """
        The properties related to the auto-storage account.
        :param pulumi.Input[str] storage_account_id: The resource ID of the storage account to be used for auto-storage account.
        """
        pulumi.set(__self__, 'storage_account_id', storage_account_id)

    @property
    @pulumi.getter(name='storageAccountId')
    def storage_account_id(self) -> pulumi.Input[str]:
        """
        The resource ID of the storage account to be used for auto-storage account.
        """
        return pulumi.get(self, 'storage_account_id')

    @storage_account_id.setter
    def storage_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'storage_account_id', value)

@pulumi.input_type
class KeyVaultReferenceArgs:

    def __init__(__self__, *, id: pulumi.Input[str], url: pulumi.Input[str]):
        """
        Identifies the Azure key vault associated with a Batch account.
        :param pulumi.Input[str] id: The resource ID of the Azure key vault associated with the Batch account.
        :param pulumi.Input[str] url: The URL of the Azure key vault associated with the Batch account.
        """
        pulumi.set(__self__, 'id', id)
        pulumi.set(__self__, 'url', url)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        The resource ID of the Azure key vault associated with the Batch account.
        """
        return pulumi.get(self, 'id')

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'id', value)

    @property
    @pulumi.getter
    def url(self) -> pulumi.Input[str]:
        """
        The URL of the Azure key vault associated with the Batch account.
        """
        return pulumi.get(self, 'url')

    @url.setter
    def url(self, value: pulumi.Input[str]):
        pulumi.set(self, 'url', value)