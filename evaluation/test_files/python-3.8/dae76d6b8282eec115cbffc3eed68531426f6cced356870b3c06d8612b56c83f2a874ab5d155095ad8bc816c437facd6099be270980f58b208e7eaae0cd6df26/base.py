from __future__ import annotations
from functools import reduce
from typing import Collection, Dict, List, Optional, cast
from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.protobuf as sp
import sarus_data_spec.query_manager.simple_rules as compilation_rules
import sarus_data_spec.typing as st

class BaseQueryManager:

    def __init__(self, storage: Storage):
        self._storage = storage

    def storage(self) -> Storage:
        return self._storage

    def is_compliant(self, dataspec: st.DataSpec, kind: st.ConstraintKind, public_context: List[str], epsilon: Optional[float]) -> bool:
        variant = self.variant(dataspec, kind, public_context, epsilon)
        if variant:
            return variant.uuid() == dataspec.uuid()
        else:
            return False

    def variant(self, dataspec: st.DataSpec, kind: st.ConstraintKind, public_context: List[str], epsilon: Optional[float]) -> Optional[st.DataSpec]:
        return compilation_rules.compile(self, dataspec, kind, public_context, epsilon)

    def variants(self, dataspec: st.DataSpec) -> Collection[st.DataSpec]:
        attributes = self.storage().referring(dataspec, type_name=sp.type_name(sp.Attribute))
        all_attributes: Dict[str, str] = reduce(lambda x, y: {**x, **y}, map(lambda x: x.properties(), attributes), dict())
        variants_uuids = [uuid for (key, uuid) in all_attributes.items() if key in sp.ConstraintKind.DESCRIPTOR.values_by_name]
        variants = [cast(st.DataSpec, self.storage().referrable(uuid)) for uuid in variants_uuids]
        return [var for var in variants if var]

    def variant_constraint(self, dataspec: st.DataSpec) -> Optional[st.VariantConstraint]:
        constraints = self.storage().referring(dataspec, type_name=sp.type_name(sp.VariantConstraint))
        if len(constraints) == 0:
            return None
        elif len(constraints) == 1:
            return cast(st.VariantConstraint, list(constraints)[0])
        else:
            raise ValueError(f'More than one variant_constraint attached to {dataspec}')

    def verifies(self, variant_constraint: st.VariantConstraint, kind: st.ConstraintKind, public_context: Collection[str], epsilon: Optional[float]) -> bool:
        return compilation_rules.verifies(query_manager=self, variant_constraint=variant_constraint, kind=kind, public_context=public_context, epsilon=epsilon)

    def is_pe_preserving(self, transform: st.Transform) -> bool:
        raise NotImplementedError('is_pe_preserving')

    def is_differentially_private(self, transform: st.Transform) -> bool:
        raise NotImplementedError('is_differentially_private')

    def transform_equivalent(self, transform: st.Transform, dp: bool) -> Optional[st.Transform]:
        """Return the DP or non-DP version of a transform.

        Return None if the requested DP equivalent does not exist.
        """
        raise NotImplementedError('transform_equivalent')