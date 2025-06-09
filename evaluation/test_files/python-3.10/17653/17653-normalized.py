def locate(self):
    """
            Lazily locates the element on the DOM if the WebElement instance is not available already.
            Returns a WebElement object.
            It also caches the element if caching has been set through cache().
        """
    if self._web_element:
        return self._web_element
    else:
        (locator_type, locator_value) = self.__locator
        element = self.driver.find_element(by=locator_type, value=locator_value)
        self._cache_web_element(element)
        return element