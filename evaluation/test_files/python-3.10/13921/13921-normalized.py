def activate_item(self, child, edit_prop=False, select=False):
    """load the selected item in the property editor"""
    d = self.tree.GetItemData(child)
    if d:
        o = d.GetData()
        self.selected_obj = o
        callback = lambda o=o, **kwargs: self.update(o, **kwargs)
        self.propeditor.load_object(o, callback)
        if edit_prop:
            wx.CallAfter(self.propeditor.edit)
        if select and self.designer:
            self.designer.select(o)
    else:
        self.selected_obj = None