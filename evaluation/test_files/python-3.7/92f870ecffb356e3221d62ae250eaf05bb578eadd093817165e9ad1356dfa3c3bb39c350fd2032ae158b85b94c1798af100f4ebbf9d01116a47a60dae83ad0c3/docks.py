class DockBase(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_container(self):
        candidate = self
        while not (candidate.__class__.__name__ == 'DockContainer' or candidate is None):
            candidate = candidate.parent()
        return candidate

    def get_dock_box(self):
        candidate = self
        while not (candidate.__class__.__name__ in ['DockVBox', 'DockHBox'] or candidate is None):
            candidate = candidate.parent()
        return candidate

    def detach(self, to_new_window=True):
        container = self.get_container()
        geo = self.geometry()
        return container.detach('layout', self.category, self.title, to_new_window, geo.width(), geo.height())