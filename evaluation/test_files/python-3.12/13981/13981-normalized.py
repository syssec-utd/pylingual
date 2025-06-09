def assert_all_of_selectors(self, selector, *locators, **kwargs):
    """
        Asserts that all of the provided selectors are present on the given page or descendants of
        the current node. If options are provided, the assertion will check that each locator is
        present with those options as well (other than ``wait``). ::

            page.assert_all_of_selectors("custom", "Tom", "Joe", visible="all")
            page.assert_all_of_selectors("css", "#my_dif", "a.not_clicked")

        It accepts all options that :meth:`find_all` accepts, such as ``text`` and ``visible``.

        The ``wait`` option applies to all of the selectors as a group, so all of the locators must
        be present within ``wait`` (defaults to :data:`capybara.default_max_wait_time`) seconds.

        If the given selector is not a valid selector, the first argument is assumed to be a locator
        and the default selector will be used.

        Args:
            selector (str, optional): The name of the selector to use. Defaults to
                :data:`capybara.default_selector`.
            *locators (str): Variable length list of locators.
            **kwargs: Arbitrary keyword arguments for :class:`SelectorQuery`.
        """
    wait = kwargs['wait'] if 'wait' in kwargs else capybara.default_max_wait_time
    if not isinstance(selector, Hashable) or selector not in selectors:
        locators = (selector,) + locators
        selector = capybara.default_selector

    @self.synchronize(wait=wait)
    def assert_all_of_selectors():
        for locator in locators:
            self.assert_selector(selector, locator, **kwargs)
        return True
    return assert_all_of_selectors()