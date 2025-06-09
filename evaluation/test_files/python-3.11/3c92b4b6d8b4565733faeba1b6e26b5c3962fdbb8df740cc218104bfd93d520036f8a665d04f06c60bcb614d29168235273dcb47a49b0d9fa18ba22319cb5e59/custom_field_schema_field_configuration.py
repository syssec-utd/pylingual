import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
__all__ = ['CustomFieldSchemaFieldConfigurationArgs', 'CustomFieldSchemaFieldConfiguration']

@pulumi.input_type
class CustomFieldSchemaFieldConfigurationArgs:

    def __init__(__self__, *, field: pulumi.Input[str], schema: pulumi.Input[str], default_value: Optional[pulumi.Input[str]]=None, default_value_datatype: Optional[pulumi.Input[str]]=None, default_value_multi_value: Optional[pulumi.Input[bool]]=None, required: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a CustomFieldSchemaFieldConfiguration resource.
        :param pulumi.Input[str] field: The ID of the field.
        :param pulumi.Input[str] schema: The ID of the schema.
        :param pulumi.Input[str] default_value: The default value for the field.
        :param pulumi.Input[str] default_value_datatype: The datatype of the default value.
        :param pulumi.Input[bool] default_value_multi_value: Whether or not the default value is multi-valued.
        :param pulumi.Input[bool] required: True if the field is required
        """
        pulumi.set(__self__, 'field', field)
        pulumi.set(__self__, 'schema', schema)
        if default_value is not None:
            pulumi.set(__self__, 'default_value', default_value)
        if default_value_datatype is not None:
            pulumi.set(__self__, 'default_value_datatype', default_value_datatype)
        if default_value_multi_value is not None:
            pulumi.set(__self__, 'default_value_multi_value', default_value_multi_value)
        if required is not None:
            pulumi.set(__self__, 'required', required)

    @property
    @pulumi.getter
    def field(self) -> pulumi.Input[str]:
        """
        The ID of the field.
        """
        return pulumi.get(self, 'field')

    @field.setter
    def field(self, value: pulumi.Input[str]):
        pulumi.set(self, 'field', value)

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Input[str]:
        """
        The ID of the schema.
        """
        return pulumi.get(self, 'schema')

    @schema.setter
    def schema(self, value: pulumi.Input[str]):
        pulumi.set(self, 'schema', value)

    @property
    @pulumi.getter(name='defaultValue')
    def default_value(self) -> Optional[pulumi.Input[str]]:
        """
        The default value for the field.
        """
        return pulumi.get(self, 'default_value')

    @default_value.setter
    def default_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_value', value)

    @property
    @pulumi.getter(name='defaultValueDatatype')
    def default_value_datatype(self) -> Optional[pulumi.Input[str]]:
        """
        The datatype of the default value.
        """
        return pulumi.get(self, 'default_value_datatype')

    @default_value_datatype.setter
    def default_value_datatype(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_value_datatype', value)

    @property
    @pulumi.getter(name='defaultValueMultiValue')
    def default_value_multi_value(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not the default value is multi-valued.
        """
        return pulumi.get(self, 'default_value_multi_value')

    @default_value_multi_value.setter
    def default_value_multi_value(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'default_value_multi_value', value)

    @property
    @pulumi.getter
    def required(self) -> Optional[pulumi.Input[bool]]:
        """
        True if the field is required
        """
        return pulumi.get(self, 'required')

    @required.setter
    def required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'required', value)

@pulumi.input_type
class _CustomFieldSchemaFieldConfigurationState:

    def __init__(__self__, *, default_value: Optional[pulumi.Input[str]]=None, default_value_datatype: Optional[pulumi.Input[str]]=None, default_value_multi_value: Optional[pulumi.Input[bool]]=None, field: Optional[pulumi.Input[str]]=None, required: Optional[pulumi.Input[bool]]=None, schema: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering CustomFieldSchemaFieldConfiguration resources.
        :param pulumi.Input[str] default_value: The default value for the field.
        :param pulumi.Input[str] default_value_datatype: The datatype of the default value.
        :param pulumi.Input[bool] default_value_multi_value: Whether or not the default value is multi-valued.
        :param pulumi.Input[str] field: The ID of the field.
        :param pulumi.Input[bool] required: True if the field is required
        :param pulumi.Input[str] schema: The ID of the schema.
        """
        if default_value is not None:
            pulumi.set(__self__, 'default_value', default_value)
        if default_value_datatype is not None:
            pulumi.set(__self__, 'default_value_datatype', default_value_datatype)
        if default_value_multi_value is not None:
            pulumi.set(__self__, 'default_value_multi_value', default_value_multi_value)
        if field is not None:
            pulumi.set(__self__, 'field', field)
        if required is not None:
            pulumi.set(__self__, 'required', required)
        if schema is not None:
            pulumi.set(__self__, 'schema', schema)

    @property
    @pulumi.getter(name='defaultValue')
    def default_value(self) -> Optional[pulumi.Input[str]]:
        """
        The default value for the field.
        """
        return pulumi.get(self, 'default_value')

    @default_value.setter
    def default_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_value', value)

    @property
    @pulumi.getter(name='defaultValueDatatype')
    def default_value_datatype(self) -> Optional[pulumi.Input[str]]:
        """
        The datatype of the default value.
        """
        return pulumi.get(self, 'default_value_datatype')

    @default_value_datatype.setter
    def default_value_datatype(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'default_value_datatype', value)

    @property
    @pulumi.getter(name='defaultValueMultiValue')
    def default_value_multi_value(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not the default value is multi-valued.
        """
        return pulumi.get(self, 'default_value_multi_value')

    @default_value_multi_value.setter
    def default_value_multi_value(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'default_value_multi_value', value)

    @property
    @pulumi.getter
    def field(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the field.
        """
        return pulumi.get(self, 'field')

    @field.setter
    def field(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'field', value)

    @property
    @pulumi.getter
    def required(self) -> Optional[pulumi.Input[bool]]:
        """
        True if the field is required
        """
        return pulumi.get(self, 'required')

    @required.setter
    def required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'required', value)

    @property
    @pulumi.getter
    def schema(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the schema.
        """
        return pulumi.get(self, 'schema')

    @schema.setter
    def schema(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'schema', value)

class CustomFieldSchemaFieldConfiguration(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, default_value: Optional[pulumi.Input[str]]=None, default_value_datatype: Optional[pulumi.Input[str]]=None, default_value_multi_value: Optional[pulumi.Input[bool]]=None, field: Optional[pulumi.Input[str]]=None, required: Optional[pulumi.Input[bool]]=None, schema: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        A [Custom Field Configuration](https://support.pagerduty.com/docs/custom-fields#associate-schemas-with-services) is a declaration of a specific Custom Field in a specific Custom Field Schema.

        > The Custom Fields feature is currently available in Early Access.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        cs_impact = pagerduty.CustomField("csImpact", datatype="string")
        my_schema = pagerduty.CustomFieldSchema("mySchema",
            title="My Schema",
            description="Fields used on incidents")
        first_field_configuration = pagerduty.CustomFieldSchemaFieldConfiguration("firstFieldConfiguration",
            schema=my_schema.id,
            field=cs_impact.id,
            required=True,
            default_value="none",
            default_value_datatype="string")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_value: The default value for the field.
        :param pulumi.Input[str] default_value_datatype: The datatype of the default value.
        :param pulumi.Input[bool] default_value_multi_value: Whether or not the default value is multi-valued.
        :param pulumi.Input[str] field: The ID of the field.
        :param pulumi.Input[bool] required: True if the field is required
        :param pulumi.Input[str] schema: The ID of the schema.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: CustomFieldSchemaFieldConfigurationArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A [Custom Field Configuration](https://support.pagerduty.com/docs/custom-fields#associate-schemas-with-services) is a declaration of a specific Custom Field in a specific Custom Field Schema.

        > The Custom Fields feature is currently available in Early Access.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        cs_impact = pagerduty.CustomField("csImpact", datatype="string")
        my_schema = pagerduty.CustomFieldSchema("mySchema",
            title="My Schema",
            description="Fields used on incidents")
        first_field_configuration = pagerduty.CustomFieldSchemaFieldConfiguration("firstFieldConfiguration",
            schema=my_schema.id,
            field=cs_impact.id,
            required=True,
            default_value="none",
            default_value_datatype="string")
        ```

        :param str resource_name: The name of the resource.
        :param CustomFieldSchemaFieldConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CustomFieldSchemaFieldConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, default_value: Optional[pulumi.Input[str]]=None, default_value_datatype: Optional[pulumi.Input[str]]=None, default_value_multi_value: Optional[pulumi.Input[bool]]=None, field: Optional[pulumi.Input[str]]=None, required: Optional[pulumi.Input[bool]]=None, schema: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CustomFieldSchemaFieldConfigurationArgs.__new__(CustomFieldSchemaFieldConfigurationArgs)
            __props__.__dict__['default_value'] = default_value
            __props__.__dict__['default_value_datatype'] = default_value_datatype
            __props__.__dict__['default_value_multi_value'] = default_value_multi_value
            if field is None and (not opts.urn):
                raise TypeError("Missing required property 'field'")
            __props__.__dict__['field'] = field
            __props__.__dict__['required'] = required
            if schema is None and (not opts.urn):
                raise TypeError("Missing required property 'schema'")
            __props__.__dict__['schema'] = schema
        super(CustomFieldSchemaFieldConfiguration, __self__).__init__('pagerduty:index/customFieldSchemaFieldConfiguration:CustomFieldSchemaFieldConfiguration', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, default_value: Optional[pulumi.Input[str]]=None, default_value_datatype: Optional[pulumi.Input[str]]=None, default_value_multi_value: Optional[pulumi.Input[bool]]=None, field: Optional[pulumi.Input[str]]=None, required: Optional[pulumi.Input[bool]]=None, schema: Optional[pulumi.Input[str]]=None) -> 'CustomFieldSchemaFieldConfiguration':
        """
        Get an existing CustomFieldSchemaFieldConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] default_value: The default value for the field.
        :param pulumi.Input[str] default_value_datatype: The datatype of the default value.
        :param pulumi.Input[bool] default_value_multi_value: Whether or not the default value is multi-valued.
        :param pulumi.Input[str] field: The ID of the field.
        :param pulumi.Input[bool] required: True if the field is required
        :param pulumi.Input[str] schema: The ID of the schema.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _CustomFieldSchemaFieldConfigurationState.__new__(_CustomFieldSchemaFieldConfigurationState)
        __props__.__dict__['default_value'] = default_value
        __props__.__dict__['default_value_datatype'] = default_value_datatype
        __props__.__dict__['default_value_multi_value'] = default_value_multi_value
        __props__.__dict__['field'] = field
        __props__.__dict__['required'] = required
        __props__.__dict__['schema'] = schema
        return CustomFieldSchemaFieldConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='defaultValue')
    def default_value(self) -> pulumi.Output[Optional[str]]:
        """
        The default value for the field.
        """
        return pulumi.get(self, 'default_value')

    @property
    @pulumi.getter(name='defaultValueDatatype')
    def default_value_datatype(self) -> pulumi.Output[Optional[str]]:
        """
        The datatype of the default value.
        """
        return pulumi.get(self, 'default_value_datatype')

    @property
    @pulumi.getter(name='defaultValueMultiValue')
    def default_value_multi_value(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not the default value is multi-valued.
        """
        return pulumi.get(self, 'default_value_multi_value')

    @property
    @pulumi.getter
    def field(self) -> pulumi.Output[str]:
        """
        The ID of the field.
        """
        return pulumi.get(self, 'field')

    @property
    @pulumi.getter
    def required(self) -> pulumi.Output[Optional[bool]]:
        """
        True if the field is required
        """
        return pulumi.get(self, 'required')

    @property
    @pulumi.getter
    def schema(self) -> pulumi.Output[str]:
        """
        The ID of the schema.
        """
        return pulumi.get(self, 'schema')