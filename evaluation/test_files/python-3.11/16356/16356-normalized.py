def about_godot(self, info):
    """ Handles displaying a view about Godot.
        """
    if info.initialized:
        self.edit_traits(parent=info.ui.control, kind='livemodal', view=about_view)