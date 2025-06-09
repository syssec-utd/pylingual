def get_ancestor_item(self, tree_alias, base_item):
    """Climbs up the site tree to resolve root item for chosen one.

        :param str|unicode tree_alias:
        :param TreeItemBase base_item:
        :rtype: TreeItemBase
        """
    parent = None
    if hasattr(base_item, 'parent') and base_item.parent is not None:
        parent = self.get_ancestor_item(tree_alias, self.get_item_by_id(tree_alias, base_item.parent.id))
    if parent is None:
        return base_item
    return parent