import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['DocumentAiProcessorDefaultVersionArgs', 'DocumentAiProcessorDefaultVersion']

@pulumi.input_type
class DocumentAiProcessorDefaultVersionArgs:

    def __init__(__self__, *, processor: pulumi.Input[str], version: pulumi.Input[str]):
        """
        The set of arguments for constructing a DocumentAiProcessorDefaultVersion resource.
        :param pulumi.Input[str] processor: The processor to set the version on.
        :param pulumi.Input[str] version: The version to set
        """
        pulumi.set(__self__, 'processor', processor)
        pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def processor(self) -> pulumi.Input[str]:
        """
        The processor to set the version on.
        """
        return pulumi.get(self, 'processor')

    @processor.setter
    def processor(self, value: pulumi.Input[str]):
        pulumi.set(self, 'processor', value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        The version to set
        """
        return pulumi.get(self, 'version')

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, 'version', value)

@pulumi.input_type
class _DocumentAiProcessorDefaultVersionState:

    def __init__(__self__, *, processor: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering DocumentAiProcessorDefaultVersion resources.
        :param pulumi.Input[str] processor: The processor to set the version on.
        :param pulumi.Input[str] version: The version to set
        """
        if processor is not None:
            pulumi.set(__self__, 'processor', processor)
        if version is not None:
            pulumi.set(__self__, 'version', version)

    @property
    @pulumi.getter
    def processor(self) -> Optional[pulumi.Input[str]]:
        """
        The processor to set the version on.
        """
        return pulumi.get(self, 'processor')

    @processor.setter
    def processor(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'processor', value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version to set
        """
        return pulumi.get(self, 'version')

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'version', value)

class DocumentAiProcessorDefaultVersion(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, processor: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        The default version for the processor. Deleting this resource is a no-op, and does not unset the default version.

        ## Example Usage
        ### Documentai Default Version

        ```python
        import pulumi
        import pulumi_gcp as gcp

        processor_document_ai_processor = gcp.essentialcontacts.DocumentAiProcessor("processorDocumentAiProcessor",
            location="us",
            display_name="test-processor",
            type="OCR_PROCESSOR")
        processor_document_ai_processor_default_version = gcp.essentialcontacts.DocumentAiProcessorDefaultVersion("processorDocumentAiProcessorDefaultVersion",
            processor=processor_document_ai_processor.id,
            version=processor_document_ai_processor.id.apply(lambda id: f"{id}/processorVersions/pretrained-next"))
        ```

        ## Import

        ProcessorDefaultVersion can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:essentialcontacts/documentAiProcessorDefaultVersion:DocumentAiProcessorDefaultVersion default {{processor}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] processor: The processor to set the version on.
        :param pulumi.Input[str] version: The version to set
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: DocumentAiProcessorDefaultVersionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The default version for the processor. Deleting this resource is a no-op, and does not unset the default version.

        ## Example Usage
        ### Documentai Default Version

        ```python
        import pulumi
        import pulumi_gcp as gcp

        processor_document_ai_processor = gcp.essentialcontacts.DocumentAiProcessor("processorDocumentAiProcessor",
            location="us",
            display_name="test-processor",
            type="OCR_PROCESSOR")
        processor_document_ai_processor_default_version = gcp.essentialcontacts.DocumentAiProcessorDefaultVersion("processorDocumentAiProcessorDefaultVersion",
            processor=processor_document_ai_processor.id,
            version=processor_document_ai_processor.id.apply(lambda id: f"{id}/processorVersions/pretrained-next"))
        ```

        ## Import

        ProcessorDefaultVersion can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:essentialcontacts/documentAiProcessorDefaultVersion:DocumentAiProcessorDefaultVersion default {{processor}}
        ```

        :param str resource_name: The name of the resource.
        :param DocumentAiProcessorDefaultVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(DocumentAiProcessorDefaultVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, processor: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DocumentAiProcessorDefaultVersionArgs.__new__(DocumentAiProcessorDefaultVersionArgs)
            if processor is None and (not opts.urn):
                raise TypeError("Missing required property 'processor'")
            __props__.__dict__['processor'] = processor
            if version is None and (not opts.urn):
                raise TypeError("Missing required property 'version'")
            __props__.__dict__['version'] = version
        super(DocumentAiProcessorDefaultVersion, __self__).__init__('gcp:essentialcontacts/documentAiProcessorDefaultVersion:DocumentAiProcessorDefaultVersion', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, processor: Optional[pulumi.Input[str]]=None, version: Optional[pulumi.Input[str]]=None) -> 'DocumentAiProcessorDefaultVersion':
        """
        Get an existing DocumentAiProcessorDefaultVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] processor: The processor to set the version on.
        :param pulumi.Input[str] version: The version to set
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _DocumentAiProcessorDefaultVersionState.__new__(_DocumentAiProcessorDefaultVersionState)
        __props__.__dict__['processor'] = processor
        __props__.__dict__['version'] = version
        return DocumentAiProcessorDefaultVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def processor(self) -> pulumi.Output[str]:
        """
        The processor to set the version on.
        """
        return pulumi.get(self, 'processor')

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        The version to set
        """
        return pulumi.get(self, 'version')