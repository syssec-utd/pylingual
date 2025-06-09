def format_extension(self):
    """The format extension of asset.
        Example::

            >>> attrs = AssetAttributes(environment, 'js/models.js.coffee')
            >>> attrs.format_extension
            '.js'

            >>> attrs = AssetAttributes(environment, 'js/lib/external.min.js.coffee')
            >>> attrs.format_extension
            '.js'
        """
    for extension in reversed(self.extensions):
        compiler = self.environment.compilers.get(extension)
        if not compiler and self.environment.mimetypes.get(extension):
            return extension