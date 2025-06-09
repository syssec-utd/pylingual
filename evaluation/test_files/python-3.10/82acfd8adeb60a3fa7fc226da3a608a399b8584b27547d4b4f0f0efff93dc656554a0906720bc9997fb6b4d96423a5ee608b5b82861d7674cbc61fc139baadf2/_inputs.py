import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['ModelTestingDatasetArgs', 'ModelTrainingDatasetArgs', 'ModelValidationDatasetArgs', 'GetModelsFilterArgs', 'GetProjectsFilterArgs']

@pulumi.input_type
class ModelTestingDatasetArgs:

    def __init__(__self__, *, dataset_type: pulumi.Input[str], bucket: Optional[pulumi.Input[str]]=None, dataset_id: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, object: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] dataset_type: Type of the Dataset.
        :param pulumi.Input[str] bucket: The name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] dataset_id: The OCID of the Data Science Labeling Dataset.
        :param pulumi.Input[str] namespace_name: The namespace name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] object: The object name of the input data file.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        pulumi.set(__self__, 'dataset_type', dataset_type)
        if bucket is not None:
            pulumi.set(__self__, 'bucket', bucket)
        if dataset_id is not None:
            pulumi.set(__self__, 'dataset_id', dataset_id)
        if namespace_name is not None:
            pulumi.set(__self__, 'namespace_name', namespace_name)
        if object is not None:
            pulumi.set(__self__, 'object', object)

    @property
    @pulumi.getter(name='datasetType')
    def dataset_type(self) -> pulumi.Input[str]:
        """
        Type of the Dataset.
        """
        return pulumi.get(self, 'dataset_type')

    @dataset_type.setter
    def dataset_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'dataset_type', value)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'bucket')

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'bucket', value)

    @property
    @pulumi.getter(name='datasetId')
    def dataset_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the Data Science Labeling Dataset.
        """
        return pulumi.get(self, 'dataset_id')

    @dataset_id.setter
    def dataset_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dataset_id', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter
    def object(self) -> Optional[pulumi.Input[str]]:
        """
        The object name of the input data file.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'object')

    @object.setter
    def object(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'object', value)

@pulumi.input_type
class ModelTrainingDatasetArgs:

    def __init__(__self__, *, dataset_type: pulumi.Input[str], bucket: Optional[pulumi.Input[str]]=None, dataset_id: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, object: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] dataset_type: Type of the Dataset.
        :param pulumi.Input[str] bucket: The name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] dataset_id: The OCID of the Data Science Labeling Dataset.
        :param pulumi.Input[str] namespace_name: The namespace name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] object: The object name of the input data file.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        pulumi.set(__self__, 'dataset_type', dataset_type)
        if bucket is not None:
            pulumi.set(__self__, 'bucket', bucket)
        if dataset_id is not None:
            pulumi.set(__self__, 'dataset_id', dataset_id)
        if namespace_name is not None:
            pulumi.set(__self__, 'namespace_name', namespace_name)
        if object is not None:
            pulumi.set(__self__, 'object', object)

    @property
    @pulumi.getter(name='datasetType')
    def dataset_type(self) -> pulumi.Input[str]:
        """
        Type of the Dataset.
        """
        return pulumi.get(self, 'dataset_type')

    @dataset_type.setter
    def dataset_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'dataset_type', value)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'bucket')

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'bucket', value)

    @property
    @pulumi.getter(name='datasetId')
    def dataset_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the Data Science Labeling Dataset.
        """
        return pulumi.get(self, 'dataset_id')

    @dataset_id.setter
    def dataset_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dataset_id', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter
    def object(self) -> Optional[pulumi.Input[str]]:
        """
        The object name of the input data file.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'object')

    @object.setter
    def object(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'object', value)

@pulumi.input_type
class ModelValidationDatasetArgs:

    def __init__(__self__, *, dataset_type: pulumi.Input[str], bucket: Optional[pulumi.Input[str]]=None, dataset_id: Optional[pulumi.Input[str]]=None, namespace_name: Optional[pulumi.Input[str]]=None, object: Optional[pulumi.Input[str]]=None):
        """
        :param pulumi.Input[str] dataset_type: Type of the Dataset.
        :param pulumi.Input[str] bucket: The name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] dataset_id: The OCID of the Data Science Labeling Dataset.
        :param pulumi.Input[str] namespace_name: The namespace name of the ObjectStorage bucket that contains the input data file.
        :param pulumi.Input[str] object: The object name of the input data file.
               
               
               ** IMPORTANT **
               Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        pulumi.set(__self__, 'dataset_type', dataset_type)
        if bucket is not None:
            pulumi.set(__self__, 'bucket', bucket)
        if dataset_id is not None:
            pulumi.set(__self__, 'dataset_id', dataset_id)
        if namespace_name is not None:
            pulumi.set(__self__, 'namespace_name', namespace_name)
        if object is not None:
            pulumi.set(__self__, 'object', object)

    @property
    @pulumi.getter(name='datasetType')
    def dataset_type(self) -> pulumi.Input[str]:
        """
        Type of the Dataset.
        """
        return pulumi.get(self, 'dataset_type')

    @dataset_type.setter
    def dataset_type(self, value: pulumi.Input[str]):
        pulumi.set(self, 'dataset_type', value)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'bucket')

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'bucket', value)

    @property
    @pulumi.getter(name='datasetId')
    def dataset_id(self) -> Optional[pulumi.Input[str]]:
        """
        The OCID of the Data Science Labeling Dataset.
        """
        return pulumi.get(self, 'dataset_id')

    @dataset_id.setter
    def dataset_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'dataset_id', value)

    @property
    @pulumi.getter(name='namespaceName')
    def namespace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace name of the ObjectStorage bucket that contains the input data file.
        """
        return pulumi.get(self, 'namespace_name')

    @namespace_name.setter
    def namespace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'namespace_name', value)

    @property
    @pulumi.getter
    def object(self) -> Optional[pulumi.Input[str]]:
        """
        The object name of the input data file.


        ** IMPORTANT **
        Any change to a property that does not support update will force the destruction and recreation of the resource with the new property values
        """
        return pulumi.get(self, 'object')

    @object.setter
    def object(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'object', value)

@pulumi.input_type
class GetModelsFilterArgs:

    def __init__(__self__, *, name: str, values: Sequence[str], regex: Optional[bool]=None):
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'values', values)
        if regex is not None:
            pulumi.set(__self__, 'regex', regex)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: str):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        return pulumi.get(self, 'values')

    @values.setter
    def values(self, value: Sequence[str]):
        pulumi.set(self, 'values', value)

    @property
    @pulumi.getter
    def regex(self) -> Optional[bool]:
        return pulumi.get(self, 'regex')

    @regex.setter
    def regex(self, value: Optional[bool]):
        pulumi.set(self, 'regex', value)

@pulumi.input_type
class GetProjectsFilterArgs:

    def __init__(__self__, *, name: str, values: Sequence[str], regex: Optional[bool]=None):
        pulumi.set(__self__, 'name', name)
        pulumi.set(__self__, 'values', values)
        if regex is not None:
            pulumi.set(__self__, 'regex', regex)

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: str):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        return pulumi.get(self, 'values')

    @values.setter
    def values(self, value: Sequence[str]):
        pulumi.set(self, 'values', value)

    @property
    @pulumi.getter
    def regex(self) -> Optional[bool]:
        return pulumi.get(self, 'regex')

    @regex.setter
    def regex(self, value: Optional[bool]):
        pulumi.set(self, 'regex', value)