import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
__all__ = ['ProductArgs', 'Product']

@pulumi.input_type
class ProductArgs:

    def __init__(__self__, *, api_management_name: pulumi.Input[str], display_name: pulumi.Input[str], product_id: pulumi.Input[str], published: pulumi.Input[bool], resource_group_name: pulumi.Input[str], approval_required: Optional[pulumi.Input[bool]]=None, description: Optional[pulumi.Input[str]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, subscriptions_limit: Optional[pulumi.Input[int]]=None, terms: Optional[pulumi.Input[str]]=None):
        """
        The set of arguments for constructing a Product resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Product.
        :param pulumi.Input[str] product_id: The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] published: Is this Product Published?
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] approval_required: Do subscribers need to be approved prior to being able to use the Product?
        :param pulumi.Input[str] description: A description of this Product, which may include HTML formatting tags.
        :param pulumi.Input[bool] subscription_required: Is a Subscription required to access API's included in this Product? Defaults to `true`.
        :param pulumi.Input[int] subscriptions_limit: The number of subscriptions a user can have to this Product at the same time.
        :param pulumi.Input[str] terms: The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        pulumi.set(__self__, 'api_management_name', api_management_name)
        pulumi.set(__self__, 'display_name', display_name)
        pulumi.set(__self__, 'product_id', product_id)
        pulumi.set(__self__, 'published', published)
        pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if approval_required is not None:
            pulumi.set(__self__, 'approval_required', approval_required)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if subscription_required is not None:
            pulumi.set(__self__, 'subscription_required', subscription_required)
        if subscriptions_limit is not None:
            pulumi.set(__self__, 'subscriptions_limit', subscriptions_limit)
        if terms is not None:
            pulumi.set(__self__, 'terms', terms)

    @property
    @pulumi.getter(name='apiManagementName')
    def api_management_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'api_management_name')

    @api_management_name.setter
    def api_management_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'api_management_name', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Input[str]:
        """
        The Display Name for this API Management Product.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='productId')
    def product_id(self) -> pulumi.Input[str]:
        """
        The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'product_id')

    @product_id.setter
    def product_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'product_id', value)

    @property
    @pulumi.getter
    def published(self) -> pulumi.Input[bool]:
        """
        Is this Product Published?
        """
        return pulumi.get(self, 'published')

    @published.setter
    def published(self, value: pulumi.Input[bool]):
        pulumi.set(self, 'published', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='approvalRequired')
    def approval_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Do subscribers need to be approved prior to being able to use the Product?
        """
        return pulumi.get(self, 'approval_required')

    @approval_required.setter
    def approval_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'approval_required', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this Product, which may include HTML formatting tags.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='subscriptionRequired')
    def subscription_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Is a Subscription required to access API's included in this Product? Defaults to `true`.
        """
        return pulumi.get(self, 'subscription_required')

    @subscription_required.setter
    def subscription_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'subscription_required', value)

    @property
    @pulumi.getter(name='subscriptionsLimit')
    def subscriptions_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The number of subscriptions a user can have to this Product at the same time.
        """
        return pulumi.get(self, 'subscriptions_limit')

    @subscriptions_limit.setter
    def subscriptions_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'subscriptions_limit', value)

    @property
    @pulumi.getter
    def terms(self) -> Optional[pulumi.Input[str]]:
        """
        The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        return pulumi.get(self, 'terms')

    @terms.setter
    def terms(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'terms', value)

@pulumi.input_type
class _ProductState:

    def __init__(__self__, *, api_management_name: Optional[pulumi.Input[str]]=None, approval_required: Optional[pulumi.Input[bool]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, published: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, subscriptions_limit: Optional[pulumi.Input[int]]=None, terms: Optional[pulumi.Input[str]]=None):
        """
        Input properties used for looking up and filtering Product resources.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] approval_required: Do subscribers need to be approved prior to being able to use the Product?
        :param pulumi.Input[str] description: A description of this Product, which may include HTML formatting tags.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Product.
        :param pulumi.Input[str] product_id: The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] published: Is this Product Published?
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] subscription_required: Is a Subscription required to access API's included in this Product? Defaults to `true`.
        :param pulumi.Input[int] subscriptions_limit: The number of subscriptions a user can have to this Product at the same time.
        :param pulumi.Input[str] terms: The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        if api_management_name is not None:
            pulumi.set(__self__, 'api_management_name', api_management_name)
        if approval_required is not None:
            pulumi.set(__self__, 'approval_required', approval_required)
        if description is not None:
            pulumi.set(__self__, 'description', description)
        if display_name is not None:
            pulumi.set(__self__, 'display_name', display_name)
        if product_id is not None:
            pulumi.set(__self__, 'product_id', product_id)
        if published is not None:
            pulumi.set(__self__, 'published', published)
        if resource_group_name is not None:
            pulumi.set(__self__, 'resource_group_name', resource_group_name)
        if subscription_required is not None:
            pulumi.set(__self__, 'subscription_required', subscription_required)
        if subscriptions_limit is not None:
            pulumi.set(__self__, 'subscriptions_limit', subscriptions_limit)
        if terms is not None:
            pulumi.set(__self__, 'terms', terms)

    @property
    @pulumi.getter(name='apiManagementName')
    def api_management_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'api_management_name')

    @api_management_name.setter
    def api_management_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'api_management_name', value)

    @property
    @pulumi.getter(name='approvalRequired')
    def approval_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Do subscribers need to be approved prior to being able to use the Product?
        """
        return pulumi.get(self, 'approval_required')

    @approval_required.setter
    def approval_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'approval_required', value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of this Product, which may include HTML formatting tags.
        """
        return pulumi.get(self, 'description')

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'description', value)

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Display Name for this API Management Product.
        """
        return pulumi.get(self, 'display_name')

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'display_name', value)

    @property
    @pulumi.getter(name='productId')
    def product_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'product_id')

    @product_id.setter
    def product_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'product_id', value)

    @property
    @pulumi.getter
    def published(self) -> Optional[pulumi.Input[bool]]:
        """
        Is this Product Published?
        """
        return pulumi.get(self, 'published')

    @published.setter
    def published(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'published', value)

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'resource_group_name', value)

    @property
    @pulumi.getter(name='subscriptionRequired')
    def subscription_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Is a Subscription required to access API's included in this Product? Defaults to `true`.
        """
        return pulumi.get(self, 'subscription_required')

    @subscription_required.setter
    def subscription_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'subscription_required', value)

    @property
    @pulumi.getter(name='subscriptionsLimit')
    def subscriptions_limit(self) -> Optional[pulumi.Input[int]]:
        """
        The number of subscriptions a user can have to this Product at the same time.
        """
        return pulumi.get(self, 'subscriptions_limit')

    @subscriptions_limit.setter
    def subscriptions_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, 'subscriptions_limit', value)

    @property
    @pulumi.getter
    def terms(self) -> Optional[pulumi.Input[str]]:
        """
        The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        return pulumi.get(self, 'terms')

    @terms.setter
    def terms(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'terms', value)

class Product(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_management_name: Optional[pulumi.Input[str]]=None, approval_required: Optional[pulumi.Input[bool]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, published: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, subscriptions_limit: Optional[pulumi.Input[int]]=None, terms: Optional[pulumi.Input[str]]=None, __props__=None):
        """
        Manages an API Management Product.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="My Company",
            publisher_email="company@exmaple.com",
            sku_name="Developer_1")
        example_product = azure.apimanagement.Product("exampleProduct",
            product_id="test-product",
            api_management_name=example_service.name,
            resource_group_name=example_resource_group.name,
            display_name="Test Product",
            subscription_required=True,
            approval_required=True,
            published=True)
        ```

        ## Import

        API Management Products can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/product:Product example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.ApiManagement/service/instance1/products/myproduct
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] approval_required: Do subscribers need to be approved prior to being able to use the Product?
        :param pulumi.Input[str] description: A description of this Product, which may include HTML formatting tags.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Product.
        :param pulumi.Input[str] product_id: The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] published: Is this Product Published?
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] subscription_required: Is a Subscription required to access API's included in this Product? Defaults to `true`.
        :param pulumi.Input[int] subscriptions_limit: The number of subscriptions a user can have to this Product at the same time.
        :param pulumi.Input[str] terms: The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: ProductArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        Manages an API Management Product.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="My Company",
            publisher_email="company@exmaple.com",
            sku_name="Developer_1")
        example_product = azure.apimanagement.Product("exampleProduct",
            product_id="test-product",
            api_management_name=example_service.name,
            resource_group_name=example_resource_group.name,
            display_name="Test Product",
            subscription_required=True,
            approval_required=True,
            published=True)
        ```

        ## Import

        API Management Products can be imported using the `resource id`, e.g.

        ```sh
         $ pulumi import azure:apimanagement/product:Product example /subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mygroup1/providers/Microsoft.ApiManagement/service/instance1/products/myproduct
        ```

        :param str resource_name: The name of the resource.
        :param ProductArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProductArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, api_management_name: Optional[pulumi.Input[str]]=None, approval_required: Optional[pulumi.Input[bool]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, published: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, subscriptions_limit: Optional[pulumi.Input[int]]=None, terms: Optional[pulumi.Input[str]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProductArgs.__new__(ProductArgs)
            if api_management_name is None and (not opts.urn):
                raise TypeError("Missing required property 'api_management_name'")
            __props__.__dict__['api_management_name'] = api_management_name
            __props__.__dict__['approval_required'] = approval_required
            __props__.__dict__['description'] = description
            if display_name is None and (not opts.urn):
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__['display_name'] = display_name
            if product_id is None and (not opts.urn):
                raise TypeError("Missing required property 'product_id'")
            __props__.__dict__['product_id'] = product_id
            if published is None and (not opts.urn):
                raise TypeError("Missing required property 'published'")
            __props__.__dict__['published'] = published
            if resource_group_name is None and (not opts.urn):
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__['resource_group_name'] = resource_group_name
            __props__.__dict__['subscription_required'] = subscription_required
            __props__.__dict__['subscriptions_limit'] = subscriptions_limit
            __props__.__dict__['terms'] = terms
        super(Product, __self__).__init__('azure:apimanagement/product:Product', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None, api_management_name: Optional[pulumi.Input[str]]=None, approval_required: Optional[pulumi.Input[bool]]=None, description: Optional[pulumi.Input[str]]=None, display_name: Optional[pulumi.Input[str]]=None, product_id: Optional[pulumi.Input[str]]=None, published: Optional[pulumi.Input[bool]]=None, resource_group_name: Optional[pulumi.Input[str]]=None, subscription_required: Optional[pulumi.Input[bool]]=None, subscriptions_limit: Optional[pulumi.Input[int]]=None, terms: Optional[pulumi.Input[str]]=None) -> 'Product':
        """
        Get an existing Product resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] approval_required: Do subscribers need to be approved prior to being able to use the Product?
        :param pulumi.Input[str] description: A description of this Product, which may include HTML formatting tags.
        :param pulumi.Input[str] display_name: The Display Name for this API Management Product.
        :param pulumi.Input[str] product_id: The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] published: Is this Product Published?
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        :param pulumi.Input[bool] subscription_required: Is a Subscription required to access API's included in this Product? Defaults to `true`.
        :param pulumi.Input[int] subscriptions_limit: The number of subscriptions a user can have to this Product at the same time.
        :param pulumi.Input[str] terms: The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = _ProductState.__new__(_ProductState)
        __props__.__dict__['api_management_name'] = api_management_name
        __props__.__dict__['approval_required'] = approval_required
        __props__.__dict__['description'] = description
        __props__.__dict__['display_name'] = display_name
        __props__.__dict__['product_id'] = product_id
        __props__.__dict__['published'] = published
        __props__.__dict__['resource_group_name'] = resource_group_name
        __props__.__dict__['subscription_required'] = subscription_required
        __props__.__dict__['subscriptions_limit'] = subscriptions_limit
        __props__.__dict__['terms'] = terms
        return Product(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='apiManagementName')
    def api_management_name(self) -> pulumi.Output[str]:
        """
        The name of the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'api_management_name')

    @property
    @pulumi.getter(name='approvalRequired')
    def approval_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Do subscribers need to be approved prior to being able to use the Product?
        """
        return pulumi.get(self, 'approval_required')

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of this Product, which may include HTML formatting tags.
        """
        return pulumi.get(self, 'description')

    @property
    @pulumi.getter(name='displayName')
    def display_name(self) -> pulumi.Output[str]:
        """
        The Display Name for this API Management Product.
        """
        return pulumi.get(self, 'display_name')

    @property
    @pulumi.getter(name='productId')
    def product_id(self) -> pulumi.Output[str]:
        """
        The Identifier for this Product, which must be unique within the API Management Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'product_id')

    @property
    @pulumi.getter
    def published(self) -> pulumi.Output[bool]:
        """
        Is this Product Published?
        """
        return pulumi.get(self, 'published')

    @property
    @pulumi.getter(name='resourceGroupName')
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the API Management Service should be exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, 'resource_group_name')

    @property
    @pulumi.getter(name='subscriptionRequired')
    def subscription_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Is a Subscription required to access API's included in this Product? Defaults to `true`.
        """
        return pulumi.get(self, 'subscription_required')

    @property
    @pulumi.getter(name='subscriptionsLimit')
    def subscriptions_limit(self) -> pulumi.Output[Optional[int]]:
        """
        The number of subscriptions a user can have to this Product at the same time.
        """
        return pulumi.get(self, 'subscriptions_limit')

    @property
    @pulumi.getter
    def terms(self) -> pulumi.Output[Optional[str]]:
        """
        The Terms and Conditions for this Product, which must be accepted by Developers before they can begin the Subscription process.
        """
        return pulumi.get(self, 'terms')