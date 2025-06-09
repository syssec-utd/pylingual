def get_summary(self):
    """
        Compat: drf-yasg 1.11
        """
    title = None
    method_name = getattr(self.view, 'action', self.method.lower())
    action = getattr(self.view, method_name, None)
    action_kwargs = getattr(action, 'kwargs', None)
    if action_kwargs:
        title = action_kwargs.get('name')
    if not title and is_custom_action(self.view.action):
        title = _(self.view.action.replace('_', ' ')).capitalize()
    if not title:
        meta = self.view.get_admin_meta()
        if self.view.action in ['retrieve', 'update', 'partial_update']:
            title = str(meta.get('verbose_name') or meta.name)
        elif self.view.action == 'create':
            title = meta.get('verbose_name')
            if title:
                title = str(_('Add')) + ' ' + str(title).lower()
            else:
                title = meta.name
        elif self.view.action == 'list':
            title = str(meta.get('verbose_name_plural') or meta.name)
        else:
            title = str(meta.name)
    return title