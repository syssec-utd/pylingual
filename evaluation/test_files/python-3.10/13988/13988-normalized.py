def has_no_unchecked_field(self, locator, **kwargs):
    """
        Checks if the page or current node has no radio button or checkbox with the given label,
        value, or id, that is currently unchecked.

        Args:
            locator (str): The label, name, or id of an unchecked field.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            bool: Whether it doesn't exist.
        """
    kwargs['checked'] = False
    return self.has_no_selector('field', locator, **kwargs)