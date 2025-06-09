import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *
__all__ = ['PrivateStoreCollectionOfferArgs', 'PrivateStoreCollectionOffer']

@pulumi.input_type
class PrivateStoreCollectionOfferArgs:

    def __init__(__self__, *, collection_id: pulumi.Input[str], private_store_id: pulumi.Input[str], e_tag: Optional[pulumi.Input[str]]=None, icon_file_uris: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, offer_id: Optional[pulumi.Input[str]]=None, plans: Optional[pulumi.Input[Sequence[pulumi.Input['PlanArgs']]]]=None, specific_plan_ids_limitation: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, update_suppressed_due_idempotence: Optional[pulumi.Input[bool]]=None):
        """
        The set of arguments for constructing a PrivateStoreCollectionOffer resource.
        :param pulumi.Input[str] collection_id: The collection ID
        :param pulumi.Input[str] private_store_id: The store ID - must use the tenant ID
        :param pulumi.Input[str] e_tag: Identifier for purposes of race condition
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] icon_file_uris: Icon File Uris
        :param pulumi.Input[str] offer_id: The offer ID to update or delete
        :param pulumi.Input[Sequence[pulumi.Input['PlanArgs']]] plans: Offer plans
        :param pulumi.Input[Sequence[pulumi.Input[str]]] specific_plan_ids_limitation: Plan ids limitation for this offer
        :param pulumi.Input[bool] update_suppressed_due_idempotence: Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        pulumi.set(__self__, 'collection_id', collection_id)
        pulumi.set(__self__, 'private_store_id', private_store_id)
        if e_tag is not None:
            pulumi.set(__self__, 'e_tag', e_tag)
        if icon_file_uris is not None:
            pulumi.set(__self__, 'icon_file_uris', icon_file_uris)
        if offer_id is not None:
            pulumi.set(__self__, 'offer_id', offer_id)
        if plans is not None:
            pulumi.set(__self__, 'plans', plans)
        if specific_plan_ids_limitation is not None:
            pulumi.set(__self__, 'specific_plan_ids_limitation', specific_plan_ids_limitation)
        if update_suppressed_due_idempotence is not None:
            pulumi.set(__self__, 'update_suppressed_due_idempotence', update_suppressed_due_idempotence)

    @property
    @pulumi.getter(name='collectionId')
    def collection_id(self) -> pulumi.Input[str]:
        """
        The collection ID
        """
        return pulumi.get(self, 'collection_id')

    @collection_id.setter
    def collection_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'collection_id', value)

    @property
    @pulumi.getter(name='privateStoreId')
    def private_store_id(self) -> pulumi.Input[str]:
        """
        The store ID - must use the tenant ID
        """
        return pulumi.get(self, 'private_store_id')

    @private_store_id.setter
    def private_store_id(self, value: pulumi.Input[str]):
        pulumi.set(self, 'private_store_id', value)

    @property
    @pulumi.getter(name='eTag')
    def e_tag(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier for purposes of race condition
        """
        return pulumi.get(self, 'e_tag')

    @e_tag.setter
    def e_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'e_tag', value)

    @property
    @pulumi.getter(name='iconFileUris')
    def icon_file_uris(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Icon File Uris
        """
        return pulumi.get(self, 'icon_file_uris')

    @icon_file_uris.setter
    def icon_file_uris(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, 'icon_file_uris', value)

    @property
    @pulumi.getter(name='offerId')
    def offer_id(self) -> Optional[pulumi.Input[str]]:
        """
        The offer ID to update or delete
        """
        return pulumi.get(self, 'offer_id')

    @offer_id.setter
    def offer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, 'offer_id', value)

    @property
    @pulumi.getter
    def plans(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PlanArgs']]]]:
        """
        Offer plans
        """
        return pulumi.get(self, 'plans')

    @plans.setter
    def plans(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PlanArgs']]]]):
        pulumi.set(self, 'plans', value)

    @property
    @pulumi.getter(name='specificPlanIdsLimitation')
    def specific_plan_ids_limitation(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Plan ids limitation for this offer
        """
        return pulumi.get(self, 'specific_plan_ids_limitation')

    @specific_plan_ids_limitation.setter
    def specific_plan_ids_limitation(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, 'specific_plan_ids_limitation', value)

    @property
    @pulumi.getter(name='updateSuppressedDueIdempotence')
    def update_suppressed_due_idempotence(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        return pulumi.get(self, 'update_suppressed_due_idempotence')

    @update_suppressed_due_idempotence.setter
    def update_suppressed_due_idempotence(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, 'update_suppressed_due_idempotence', value)

class PrivateStoreCollectionOffer(pulumi.CustomResource):

    @overload
    def __init__(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, collection_id: Optional[pulumi.Input[str]]=None, e_tag: Optional[pulumi.Input[str]]=None, icon_file_uris: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, offer_id: Optional[pulumi.Input[str]]=None, plans: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PlanArgs']]]]]=None, private_store_id: Optional[pulumi.Input[str]]=None, specific_plan_ids_limitation: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, update_suppressed_due_idempotence: Optional[pulumi.Input[bool]]=None, __props__=None):
        """
        The privateStore offer data structure.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collection_id: The collection ID
        :param pulumi.Input[str] e_tag: Identifier for purposes of race condition
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] icon_file_uris: Icon File Uris
        :param pulumi.Input[str] offer_id: The offer ID to update or delete
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PlanArgs']]]] plans: Offer plans
        :param pulumi.Input[str] private_store_id: The store ID - must use the tenant ID
        :param pulumi.Input[Sequence[pulumi.Input[str]]] specific_plan_ids_limitation: Plan ids limitation for this offer
        :param pulumi.Input[bool] update_suppressed_due_idempotence: Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        ...

    @overload
    def __init__(__self__, resource_name: str, args: PrivateStoreCollectionOfferArgs, opts: Optional[pulumi.ResourceOptions]=None):
        """
        The privateStore offer data structure.

        :param str resource_name: The name of the resource.
        :param PrivateStoreCollectionOfferArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...

    def __init__(__self__, resource_name: str, *args, **kwargs):
        (resource_args, opts) = _utilities.get_resource_args_opts(PrivateStoreCollectionOfferArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__, resource_name: str, opts: Optional[pulumi.ResourceOptions]=None, collection_id: Optional[pulumi.Input[str]]=None, e_tag: Optional[pulumi.Input[str]]=None, icon_file_uris: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]=None, offer_id: Optional[pulumi.Input[str]]=None, plans: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PlanArgs']]]]]=None, private_store_id: Optional[pulumi.Input[str]]=None, specific_plan_ids_limitation: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]=None, update_suppressed_due_idempotence: Optional[pulumi.Input[bool]]=None, __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PrivateStoreCollectionOfferArgs.__new__(PrivateStoreCollectionOfferArgs)
            if collection_id is None and (not opts.urn):
                raise TypeError("Missing required property 'collection_id'")
            __props__.__dict__['collection_id'] = collection_id
            __props__.__dict__['e_tag'] = e_tag
            __props__.__dict__['icon_file_uris'] = icon_file_uris
            __props__.__dict__['offer_id'] = offer_id
            __props__.__dict__['plans'] = plans
            if private_store_id is None and (not opts.urn):
                raise TypeError("Missing required property 'private_store_id'")
            __props__.__dict__['private_store_id'] = private_store_id
            __props__.__dict__['specific_plan_ids_limitation'] = specific_plan_ids_limitation
            __props__.__dict__['update_suppressed_due_idempotence'] = update_suppressed_due_idempotence
            __props__.__dict__['created_at'] = None
            __props__.__dict__['modified_at'] = None
            __props__.__dict__['name'] = None
            __props__.__dict__['offer_display_name'] = None
            __props__.__dict__['publisher_display_name'] = None
            __props__.__dict__['system_data'] = None
            __props__.__dict__['type'] = None
            __props__.__dict__['unique_offer_id'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_='azure-native:marketplace:PrivateStoreCollectionOffer'), pulumi.Alias(type_='azure-native:marketplace/v20211201:PrivateStoreCollectionOffer'), pulumi.Alias(type_='azure-native:marketplace/v20220301:PrivateStoreCollectionOffer'), pulumi.Alias(type_='azure-native:marketplace/v20220901:PrivateStoreCollectionOffer')])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateStoreCollectionOffer, __self__).__init__('azure-native:marketplace/v20210601:PrivateStoreCollectionOffer', resource_name, __props__, opts)

    @staticmethod
    def get(resource_name: str, id: pulumi.Input[str], opts: Optional[pulumi.ResourceOptions]=None) -> 'PrivateStoreCollectionOffer':
        """
        Get an existing PrivateStoreCollectionOffer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        __props__ = PrivateStoreCollectionOfferArgs.__new__(PrivateStoreCollectionOfferArgs)
        __props__.__dict__['created_at'] = None
        __props__.__dict__['e_tag'] = None
        __props__.__dict__['icon_file_uris'] = None
        __props__.__dict__['modified_at'] = None
        __props__.__dict__['name'] = None
        __props__.__dict__['offer_display_name'] = None
        __props__.__dict__['plans'] = None
        __props__.__dict__['private_store_id'] = None
        __props__.__dict__['publisher_display_name'] = None
        __props__.__dict__['specific_plan_ids_limitation'] = None
        __props__.__dict__['system_data'] = None
        __props__.__dict__['type'] = None
        __props__.__dict__['unique_offer_id'] = None
        __props__.__dict__['update_suppressed_due_idempotence'] = None
        return PrivateStoreCollectionOffer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name='createdAt')
    def created_at(self) -> pulumi.Output[str]:
        """
        Private store offer creation date
        """
        return pulumi.get(self, 'created_at')

    @property
    @pulumi.getter(name='eTag')
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        Identifier for purposes of race condition
        """
        return pulumi.get(self, 'e_tag')

    @property
    @pulumi.getter(name='iconFileUris')
    def icon_file_uris(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Icon File Uris
        """
        return pulumi.get(self, 'icon_file_uris')

    @property
    @pulumi.getter(name='modifiedAt')
    def modified_at(self) -> pulumi.Output[str]:
        """
        Private store offer modification date
        """
        return pulumi.get(self, 'modified_at')

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, 'name')

    @property
    @pulumi.getter(name='offerDisplayName')
    def offer_display_name(self) -> pulumi.Output[str]:
        """
        It will be displayed prominently in the marketplace
        """
        return pulumi.get(self, 'offer_display_name')

    @property
    @pulumi.getter
    def plans(self) -> pulumi.Output[Optional[Sequence['outputs.PlanResponse']]]:
        """
        Offer plans
        """
        return pulumi.get(self, 'plans')

    @property
    @pulumi.getter(name='privateStoreId')
    def private_store_id(self) -> pulumi.Output[str]:
        """
        Private store unique id
        """
        return pulumi.get(self, 'private_store_id')

    @property
    @pulumi.getter(name='publisherDisplayName')
    def publisher_display_name(self) -> pulumi.Output[str]:
        """
        Publisher name that will be displayed prominently in the marketplace
        """
        return pulumi.get(self, 'publisher_display_name')

    @property
    @pulumi.getter(name='specificPlanIdsLimitation')
    def specific_plan_ids_limitation(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Plan ids limitation for this offer
        """
        return pulumi.get(self, 'specific_plan_ids_limitation')

    @property
    @pulumi.getter(name='systemData')
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource
        """
        return pulumi.get(self, 'system_data')

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, 'type')

    @property
    @pulumi.getter(name='uniqueOfferId')
    def unique_offer_id(self) -> pulumi.Output[str]:
        """
        Offers unique id
        """
        return pulumi.get(self, 'unique_offer_id')

    @property
    @pulumi.getter(name='updateSuppressedDueIdempotence')
    def update_suppressed_due_idempotence(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        return pulumi.get(self, 'update_suppressed_due_idempotence')