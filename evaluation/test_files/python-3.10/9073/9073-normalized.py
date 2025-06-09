def get(self, *args, **kwargs):
    """ Execute the correct handler depending on what is connecting. """
    if self.is_websocket():
        return super(DemoHandler, self).get(*args, **kwargs)
    else:
        self.write(self.view.render())