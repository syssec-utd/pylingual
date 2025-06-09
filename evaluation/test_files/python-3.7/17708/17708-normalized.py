def register_defaults(self):
    """Register :class:`~gears.processors.DirectivesProcessor` as
        a preprocessor for `text/css` and `application/javascript` MIME types.
        """
    self.register('text/css', DirectivesProcessor.as_handler())
    self.register('application/javascript', DirectivesProcessor.as_handler())