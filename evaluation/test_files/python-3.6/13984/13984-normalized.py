def assert_matches_selector(self, *args, **kwargs):
    """
        Asserts that the current node matches a given selector. ::

            node.assert_matches_selector("p#foo")
            node.assert_matches_selector("xpath", "//p[@id='foo']")

        It also accepts all options that :meth:`find_all` accepts, such as ``text`` and
        ``visible``. ::

            node.assert_matches_selector("li", text="Horse", visible=True)

        Args:
            *args: Variable length argument list for :class:`SelectorQuery`.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.

        Returns:
            True

        Raises:
            ExpectationNotMet: If the selector does not match.
        """
    query = SelectorQuery(*args, **kwargs)

    @self.synchronize(wait=query.wait)
    def assert_matches_selector():
        result = query.resolve_for(self.find_first('xpath', './parent::*', minimum=0) or self.query_scope)
        if self not in result:
            raise ExpectationNotMet('Item does not match the provided selector')
        return True
    return assert_matches_selector()