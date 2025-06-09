def tree(self, tree_alias, context):
    """Builds and returns tree structure for 'sitetree_tree' tag.

        :param str|unicode tree_alias:
        :param Context context:
        :rtype: list|str
        """
    tree_alias, sitetree_items = self.init_tree(tree_alias, context)
    if not sitetree_items:
        return ''
    tree_items = self.filter_items(self.get_children(tree_alias, None), 'sitetree')
    tree_items = self.apply_hook(tree_items, 'sitetree')
    self.update_has_children(tree_alias, tree_items, 'sitetree')
    return tree_items