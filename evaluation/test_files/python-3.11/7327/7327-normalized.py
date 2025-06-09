def filter_items(self, items, navigation_type=None):
    """Filters sitetree item's children if hidden and by navigation type.

        NB: We do not apply any filters to sitetree in admin app.

        :param list items:
        :param str|unicode navigation_type: sitetree, breadcrumbs, menu
        :rtype: list
        """
    if self.current_app_is_admin():
        return items
    items_filtered = []
    context = self.current_page_context
    check_access = self.check_access
    for item in items:
        if item.hidden:
            continue
        if not check_access(item, context):
            continue
        if not getattr(item, 'in%s' % navigation_type, True):
            continue
        items_filtered.append(item)
    return items_filtered