import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['TaxonomyArgs', 'Taxonomy']

@pulumi.input_type
class TaxonomyArgs:

    def __init__(__self__, *, display_name: pulumi.Input[str], activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, description: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Taxonomy resource.
        :param pulumi.Input[str] display_name: User defined name of this taxonomy.
               It must: contain only unicode letters, numbers, underscores, dashes
               and spaces; not start or end with spaces; and be at most 200 bytes
               long when encoded in UTF-8.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] activated_policy_types: A list of policy types that are activated for this taxonomy. If not set,
               defaults to an empty list.
               Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        :param pulumi.Input[str] description: Description of this taxonomy. It must: contain only unicode characters,
               tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
               long when encoded in UTF-8. If not set, defaults to an empty description.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Taxonomy location region.
        """
        pulumi.set(__self__, 'display_name', display_name)
        if activated_policy_types is not None:
            pulumi.set(__self__, 'activated_policy_types', activated_policy_types)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if region is not None:
            pulumi.set(__self__, 'region', region)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        User defined name of this taxonomy.
        It must: contain only unicode letters, numbers, underscores, dashes
        and spaces; not start or end with spaces; and be at most 200 bytes
        long when encoded in UTF-8.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='activatedPolicyTypes')
    def activated_policy_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of policy types that are activated for this taxonomy. If not set,
        defaults to an empty list.
        Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        """
        return pulumi.get(self, 'activated_policy_types')

    @activated_policy_types.setter
    def activated_policy_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'activated_policy_types', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of this taxonomy. It must: contain only unicode characters,
        tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
        long when encoded in UTF-8. If not set, defaults to an empty description.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Taxonomy location region.
        """
        return pulumi.get(self, 'region')

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'region', value)

@pulumi.input_type
class _TaxonomyState:

    def __init__(__self__, *, activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering Taxonomy resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] activated_policy_types: A list of policy types that are activated for this taxonomy. If not set,
               defaults to an empty list.
               Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        :param pulumi.Input[str] description: Description of this taxonomy. It must: contain only unicode characters,
               tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
               long when encoded in UTF-8. If not set, defaults to an empty description.
        :param pulumi.Input[str] display_name: User defined name of this taxonomy.
               It must: contain only unicode letters, numbers, underscores, dashes
               and spaces; not start or end with spaces; and be at most 200 bytes
               long when encoded in UTF-8.
        :param pulumi.Input[str] name: Resource name of this taxonomy, whose format is: "projects/{project}/locations/{region}/taxonomies/{taxonomy}".
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Taxonomy location region.
        """
        if activated_policy_types is not None:
            pulumi.set(__self__, 'activated_policy_types', activated_policy_types)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if name is not None:
            pulumi.set(__self__, 'name', name)
        if project is not None:
            pulumi.set(__self__, 'project', project)
        if region is not None:
            pulumi.set(__self__, 'region', region)

    @property
    @pulumi.getter(name='activatedPolicyTypes')
    def activated_policy_types(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of policy types that are activated for this taxonomy. If not set,
        defaults to an empty list.
        Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        """
        return pulumi.get(self, 'activated_policy_types')

    @activated_policy_types.setter
    def activated_policy_types(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'activated_policy_types', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of this taxonomy. It must: contain only unicode characters,
        tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
        long when encoded in UTF-8. If not set, defaults to an empty description.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        User defined name of this taxonomy.
        It must: contain only unicode letters, numbers, underscores, dashes
        and spaces; not start or end with spaces; and be at most 200 bytes
        long when encoded in UTF-8.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name of this taxonomy, whose format is: "projects/{project}/locations/{region}/taxonomies/{taxonomy}".
        """
        return pulumi.get(self, 'name')

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'name', value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'project', value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        Taxonomy location region.
        """
        return pulumi.get(self, 'region')

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'region', value)

class Taxonomy(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        A collection of policy tags that classify data along a common axis.

        To get more information about Taxonomy, see:

        * [API documentation](https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.taxonomies)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/data-catalog/docs)

        ## Example Usage
        ### Data Catalog Taxonomy Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_taxonomy = gcp.datacatalog.Taxonomy("basicTaxonomy",
            region="us",
            display_name="my_display_name",
            description="A collection of policy tags",
            activated_policy_types=["FINE_GRAINED_ACCESS_CONTROL"],
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Taxonomy can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:datacatalog/taxonomy:Taxonomy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] activated_policy_types: A list of policy types that are activated for this taxonomy. If not set,
               defaults to an empty list.
               Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        :param pulumi.Input[str] description: Description of this taxonomy. It must: contain only unicode characters,
               tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
               long when encoded in UTF-8. If not set, defaults to an empty description.
        :param pulumi.Input[str] display_name: User defined name of this taxonomy.
               It must: contain only unicode letters, numbers, underscores, dashes
               and spaces; not start or end with spaces; and be at most 200 bytes
               long when encoded in UTF-8.
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Taxonomy location region.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: TaxonomyArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        A collection of policy tags that classify data along a common axis.

        To get more information about Taxonomy, see:

        * [API documentation](https://cloud.google.com/data-catalog/docs/reference/rest/v1beta1/projects.locations.taxonomies)
        * How-to Guides
            * [Official Documentation](https://cloud.google.com/data-catalog/docs)

        ## Example Usage
        ### Data Catalog Taxonomy Basic

        ```python
        import pulumi
        import pulumi_gcp as gcp

        basic_taxonomy = gcp.datacatalog.Taxonomy("basicTaxonomy",
            region="us",
            display_name="my_display_name",
            description="A collection of policy tags",
            activated_policy_types=["FINE_GRAINED_ACCESS_CONTROL"],
            opts=pulumi.ResourceOptions(provider=google_beta))
        ```

        ## Import

        Taxonomy can be imported using any of these accepted formats

        ```sh
         $ pulumi import gcp:datacatalog/taxonomy:Taxonomy default {{name}}
        ```

        :param str resource_name: The name of the resource.
        :param TaxonomyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(TaxonomyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TaxonomyArgs.__new__(TaxonomyArgs)
            __props__.__dict__['activated_policy_types'] = activated_policy_types
            __props__.__dict__['description'] = description
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            __props__.__dict__['project'] = project
            __props__.__dict__['region'] = region
            __props__.__dict__['name'] = None
        super(Taxonomy, __self__).__init__('gcp:datacatalog/taxonomy:Taxonomy', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, activated_policy_types: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, name: Optional[pulumi.Input[str]]=None, project: Optional[pulumi.Input[str]]=None, region: Optional[pulumi.Input[str]]=None) -> 'Taxonomy':
        """
        Get an existing Taxonomy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] activated_policy_types: A list of policy types that are activated for this taxonomy. If not set,
               defaults to an empty list.
               Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        :param pulumi.Input[str] description: Description of this taxonomy. It must: contain only unicode characters,
               tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
               long when encoded in UTF-8. If not set, defaults to an empty description.
        :param pulumi.Input[str] display_name: User defined name of this taxonomy.
               It must: contain only unicode letters, numbers, underscores, dashes
               and spaces; not start or end with spaces; and be at most 200 bytes
               long when encoded in UTF-8.
        :param pulumi.Input[str] name: Resource name of this taxonomy, whose format is: "projects/{project}/locations/{region}/taxonomies/{taxonomy}".
        :param pulumi.Input[str] project: The ID of the project in which the resource belongs.
               If it is not provided, the provider project is used.
        :param pulumi.Input[str] region: Taxonomy location region.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _TaxonomyState.__new__(_TaxonomyState)
        __props__.__dict__['activated_policy_types'] = activated_policy_types
        __props__.__dict__['description'] = description
        __props__.__dict__['display_name'] = display_name
        __props__.__dict__['name'] = name
        __props__.__dict__['project'] = project
        __props__.__dict__['region'] = region
        return Taxonomy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='activatedPolicyTypes')
    def activated_policy_types(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of policy types that are activated for this taxonomy. If not set,
        defaults to an empty list.
        Each value may be one of `POLICY_TYPE_UNSPECIFIED` and `FINE_GRAINED_ACCESS_CONTROL`.
        """
        return pulumi.get(self, 'activated_policy_types')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of this taxonomy. It must: contain only unicode characters,
        tabs, newlines, carriage returns and page breaks; and be at most 2000 bytes
        long when encoded in UTF-8. If not set, defaults to an empty description.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        User defined name of this taxonomy.
        It must: contain only unicode letters, numbers, underscores, dashes
        and spaces; not start or end with spaces; and be at most 200 bytes
        long when encoded in UTF-8.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name of this taxonomy, whose format is: "projects/{project}/locations/{region}/taxonomies/{taxonomy}".
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        return pulumi.get(self, 'project')

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        Taxonomy location region.
        """
        return pulumi.get(self, 'region')