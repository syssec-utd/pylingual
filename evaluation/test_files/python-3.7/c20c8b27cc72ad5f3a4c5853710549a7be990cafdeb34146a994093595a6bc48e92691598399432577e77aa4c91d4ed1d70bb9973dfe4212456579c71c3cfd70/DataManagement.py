from __future__ import annotations
from tcsoa.gen.BusinessObjects import BusinessObject, ImanRelation, Dataset
from typing import List
from tcsoa.gen.Core._2007_06.DataManagement import RelationAndTypesFilter
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass

@dataclass
class ExpandGRMRelationsData2(TcBaseObj):
    """
    The data returned from 'expandGRMRelationsPrimary' and 'expandGRMRelationsSecondary' operations.
    
    :var relationshipObjects: The list of relation objects for the relationships between the input object and side
    objects.
    :var relationName: The input Generic Relationship Manager (GRM) relation type name.
    """
    relationshipObjects: List[ExpandGRMRelationship] = ()
    relationName: str = ''

@dataclass
class ExpandGRMRelationsOutput2(TcBaseObj):
    """
    The output from 'expandGRMRelationsPrimary' and 'expandGRMRelationsSecondary' operations.
    
    :var inputObject: The object that was input to be expanded.
    :var relationshipData: The list of data for relationships between the input object and found side objects.
    """
    inputObject: BusinessObject = None
    relationshipData: List[ExpandGRMRelationsData2] = ()

@dataclass
class ExpandGRMRelationsPref2(TcBaseObj):
    """
    Preference structure for 'expandGRMRelationsPrimary' and 'expandGRMRelationsSecondary'.
    
    :var expItemRev: Flag that if true signifies that any item revisions that are in the return data should be expanded.
    :var returnRelations: Flag that if true signifies that the relation objects should be returned.
    :var info: The list of relation type and primary or secondary object type filters, depending on whether
    'expandGRMRelationsForPrimary' or 'expandGRMRelationsForSecondary' is called.  This input must be specified or
    error 214160 will be returned.  For 'expandGRMRelationsForPrimary', if all secondary objects should be returned,
    'RelationAndTypesFilter' input parameters should be empty.  For 'expandGRMRelationsForSecondary', if all primary
    objects should be returned, 'RelationAndTypesFilter' input parameters should be empty.
    """
    expItemRev: bool = False
    returnRelations: bool = False
    info: List[RelationAndTypesFilter] = ()

@dataclass
class ExpandGRMRelationsResponse2(TcBaseObj):
    """
    The response from 'expandGRMRelationsPrimary' and 'expandGRMRelationsSecondary' operations.
    
    :var output: The list of input objects and the found related side objects.
    :var serviceData: The 'ServiceData'.  This operation will populate the 'ServiceData' with the input object, any
    found side object and any found relation object.  All objects are added as plain objects.
    """
    output: List[ExpandGRMRelationsOutput2] = ()
    serviceData: ServiceData = None

@dataclass
class ExpandGRMRelationship(TcBaseObj):
    """
    The relation information returned from 'expandGRMRelationsPrimary' and 'expandGRMRelationsSecondary' operations.
    
    :var otherSideObject: The found side object.
    :var relation: The found relation object for the side object to primary object relationship.
    """
    otherSideObject: BusinessObject = None
    relation: ImanRelation = None

@dataclass
class NamedReferenceInfo(TcBaseObj):
    """
    This structure contains information for NamedReference to be removed.
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var type: Remove all 'NamedReference's of this reference name ( required )
    :var targetObject: Target object of a specific 'NamedReference' to remove ( optional, must match type above ) ) If
    specified then only this specific 'NamedReference' will be removed; other 'NamedReferences' of the same type will
    not be effected.
    :var deleteTarget: Flag to indicate if 'targetObject' is to be deleted
    """
    clientId: str = ''
    type: str = ''
    targetObject: BusinessObject = None
    deleteTarget: bool = False

@dataclass
class RemoveNamedReferenceFromDatasetInfo(TcBaseObj):
    """
    Input structure for the 'removeNamedReferenceFromDataset' operation
    
    :var clientId: A unique string supplied by the caller.  This ID is used to identify return data elements and
    partial errors associated with this input structure.  If 'clientId' is not provided then it can be difficult to
    align the input with any returned errors.
    :var dataset: The dataset object from which to remove the specified named references.
    :var nrInfo: A list of named reference information.
    """
    clientId: str = ''
    dataset: Dataset = None
    nrInfo: List[NamedReferenceInfo] = ()