def tree(alias, title='', items=None, **kwargs):
    """Dynamically creates and returns a sitetree.

    :param str|unicode alias:
    :param str|unicode title:
    :param iterable items: dynamic sitetree items objects created by `item` function.
    :param kwargs: Additional arguments to pass to tree item initializer.

    :rtype: TreeBase
    """
    tree_obj = get_tree_model()(alias=alias, title=title, **kwargs)
    tree_obj.id = generate_id_for(tree_obj)
    tree_obj.is_dynamic = True
    if items is not None:
        tree_obj.dynamic_items = []

        def traverse(items):
            for item in items:
                item.tree = tree_obj
                tree_obj.dynamic_items.append(item)
                if hasattr(item, 'dynamic_children'):
                    traverse(item.dynamic_children)
        traverse(items)
    return tree_obj