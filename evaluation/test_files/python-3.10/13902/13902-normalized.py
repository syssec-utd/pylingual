def _set_icon(self, icon=None):
    """Set icon based on resource values"""
    if icon is not None:
        try:
            wx_icon = wx.Icon(icon, wx.BITMAP_TYPE_ICO)
            self.wx_obj.SetIcon(wx_icon)
        except:
            pass