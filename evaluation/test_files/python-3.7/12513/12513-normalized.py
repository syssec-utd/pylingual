def _add_leaf_from_storage(self, args, kwargs):
    """Can be called from storage service to create a new leaf to bypass name checking"""
    return self._nn_interface._add_generic(self, type_name=LEAF, group_type_name=GROUP, args=args, kwargs=kwargs, add_prefix=False, check_naming=False)