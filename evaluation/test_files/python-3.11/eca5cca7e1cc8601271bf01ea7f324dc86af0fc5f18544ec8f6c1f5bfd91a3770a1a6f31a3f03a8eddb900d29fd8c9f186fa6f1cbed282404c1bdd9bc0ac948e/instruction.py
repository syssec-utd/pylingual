import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['InstructionArgs', 'Instruction']

@pulumi.input_type
class InstructionArgs:

    def __init__(__self__, *, data_type: pulumi.Input['InstructionDataType'], display_name: pulumi.Input[str], csv_instruction: Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']]=None, description: Optional[pulumi.Input[str]]=None, pdf_instruction: Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']]=None, project: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Instruction resource.
        :param pulumi.Input['InstructionDataType'] data_type: The data type of this instruction.
        :param pulumi.Input[str] display_name: The display name of the instruction. Maximum of 64 characters.
        :param pulumi.Input['GoogleCloudDatalabelingV1beta1CsvInstructionArgs'] csv_instruction: Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.
        :param pulumi.Input[str] description: Optional. User-provided description of the instruction. The description can be up to 10000 characters long.
        :param pulumi.Input['GoogleCloudDatalabelingV1beta1PdfInstructionArgs'] pdf_instruction: Instruction from a PDF document. The PDF should be in a Cloud Storage bucket.
        """
        pulumi.set(__self__, 'data_type', data_type)
        pulumi.set(__self__, 'display_name', display_name)
        if csv_instruction is not None:
            warnings.warn('Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.', DeprecationWarning)
            pulumi.log.warn('csv_instruction is deprecated: Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.')
        if csv_instruction is not None:
            pulumi.set(__self__, 'csv_instruction', csv_instruction)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if pdf_instruction is not None:
            pulumi.set(__self__, 'pdf_instruction', pdf_instruction)
        if project is not None:
            pulumi.set(__self__, 'project', project)

    @property
    @pulumi.getter(name='dataType')
    def data_type(self) -> pulumi.Input['InstructionDataType']:
        """
        The data type of this instruction.
        """
        return pulumi.get(self, 'data_type')

    @data_type.setter
    def data_type(self, value: pulumi.Input['InstructionDataType']):
        pulumi.set(self, 'data_type', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        The display name of the instruction. Maximum of 64 characters.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='csvInstruction')
    def csv_instruction(self) -> Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']]:
        """
        Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.
        """
        return pulumi.get(self, 'csv_instruction')

    @csv_instruction.setter
    def csv_instruction(self, value: Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']]):
        pulumi.set(self, 'csv_instruction', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional. User-provided description of the instruction. The description can be up to 10000 characters long.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='pdfInstruction')
    def pdf_instruction(self) -> Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']]:
        """
        Instruction from a PDF document. The PDF should be in a Cloud Storage bucket.
        """
        return pulumi.get(self, 'pdf_instruction')

    @pdf_instruction.setter
    def pdf_instruction(self, value: Optional[pulumi.Input['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']]):
        pulumi.set(self, 'pdf_instruction', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

class Instruction(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, csv_instruction: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']]]=None, data_type: Optional[pulumi.Input['InstructionDataType']]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, pdf_instruction: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']]]=None, project: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Creates an instruction for how data should be labeled.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']] csv_instruction: Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.
        :param pulumi.Input['InstructionDataType'] data_type: The data type of this instruction.
        :param pulumi.Input[str] description: Optional. User-provided description of the instruction. The description can be up to 10000 characters long.
        :param pulumi.Input[str] display_name: The display name of the instruction. Maximum of 64 characters.
        :param pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']] pdf_instruction: Instruction from a PDF document. The PDF should be in a Cloud Storage bucket.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: InstructionArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Creates an instruction for how data should be labeled.
        Auto-naming is currently not supported for this resource.

        :param str resource_name: The name of the resource.
        :param InstructionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstructionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, csv_instruction: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1CsvInstructionArgs']]]=None, data_type: Optional[pulumi.Input['InstructionDataType']]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, pdf_instruction: Optional[pulumi.Input[pulumi.InputType['GoogleCloudDatalabelingV1beta1PdfInstructionArgs']]]=None, project: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstructionArgs.__new__(InstructionArgs)
            if csv_instruction is not None and (not opts.urn):
                warnings.warn('Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.', DeprecationWarning)
                pulumi.log.warn('csv_instruction is deprecated: Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.')
            __props__.__dict__['csv_instruction'] = csv_instruction
            if data_type is None and (not opts.urn):
                raise TypeError("Missing required property 'data_type'")
            __props__.__dict__['data_type'] = data_type
            __props__.__dict__['description'] = description
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['pdf_instruction'] = pdf_instruction
            __props__.__dict__['project'] = project
            __props__.__dict__['blocking_resources'] = None
            __props__.__dict__['create_time'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['update_time'] = None
        replace_on_changes = pulumi.ResourceOptions(replace_on_changes=['project'])
        opts = pulumi.ResourceOptions.merge(opts, replace_on_changes)
        super(Instruction, __self__).__init__('google-native:datalabeling/v1beta1:Instruction', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'Instruction':
        """
        Get an existing Instruction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = InstructionArgs.__new__(InstructionArgs)
        __props__.__dict__['blocking_resources'] = None
        __props__.__dict__['create_time'] = None
        __props__.__dict__['csv_instruction'] = None
        __props__.__dict__['data_type'] = None
        __props__.__dict__['description'] = None
        __props__.__dict__['display_name'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['pdf_instruction'] = None
        __props__.__dict__['project'] = None
        __props__.__dict__['update_time'] = None
        return Instruction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='blockingResources')
    def blocking_resources(self) -> pulumi.Output[Sequence[str]]:
        """
        The names of any related resources that are blocking changes to the instruction.
        """
        return pulumi.get(self, 'blocking_resources')

    @property
    @pulumi.getter(name='createTime')
    def create_time(self) -> pulumi.Output[str]:
        """
        Creation time of instruction.
        """
        return pulumi.get(self, 'create_time')

    @property
    @pulumi.getter(name='csvInstruction')
    def csv_instruction(self) -> pulumi.Output['outputs.GoogleCloudDatalabelingV1beta1CsvInstructionResponse']:
        """
        Deprecated: this instruction format is not supported any more. Instruction from a CSV file, such as for classification task. The CSV file should have exact two columns, in the following format: * The first column is labeled data, such as an image reference, text. * The second column is comma separated labels associated with data.
        """
        return pulumi.get(self, 'csv_instruction')

    @property
    @pulumi.getter(name='dataType')
    def data_type(self) -> pulumi.Output[str]:
        """
        The data type of this instruction.
        """
        return pulumi.get(self, 'data_type')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Optional. User-provided description of the instruction. The description can be up to 10000 characters long.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of the instruction. Maximum of 64 characters.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Instruction resource name, format: projects/{project_id}/instructions/{instruction_id}
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='pdfInstruction')
    def pdf_instruction(self) -> pulumi.Output['outputs.GoogleCloudDatalabelingV1beta1PdfInstructionResponse']:
        """
        Instruction from a PDF document. The PDF should be in a Cloud Storage bucket.
        """
        return pulumi.get(self, 'pdf_instruction')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter(name='updateTime')
    def update_time(self) -> pulumi.Output[str]:
        """
        Last update time of instruction.
        """
        return pulumi.get(self, 'update_time')