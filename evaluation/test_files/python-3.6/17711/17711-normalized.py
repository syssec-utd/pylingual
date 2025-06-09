def register_defaults(self):
    """Register default compilers, preprocessors and MIME types."""
    self.mimetypes.register_defaults()
    self.preprocessors.register_defaults()
    self.postprocessors.register_defaults()