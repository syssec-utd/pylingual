def _merge_perm(self, permission_name, view_menu_name):
    """
        Add the new permission , view_menu to ab_permission_view_role if not exists.
        It will add the related entry to ab_permission
        and ab_view_menu two meta tables as well.

        :param permission_name: Name of the permission.
        :type permission_name: str
        :param view_menu_name: Name of the view-menu
        :type view_menu_name: str
        :return:
        """
    permission = self.find_permission(permission_name)
    view_menu = self.find_view_menu(view_menu_name)
    pv = None
    if permission and view_menu:
        pv = self.get_session.query(self.permissionview_model).filter_by(permission=permission, view_menu=view_menu).first()
    if not pv and permission_name and view_menu_name:
        self.add_permission_view_menu(permission_name, view_menu_name)