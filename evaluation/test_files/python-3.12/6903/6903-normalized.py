def standard(cls, element):
    """
        Implement the standard and alphabetical sorting.

        :param element: The element we are currently reading.
        :type element: str

        :return: The formatted element.
        :rtype: str
        """
    return Regex(element, cls.regex_replace, replace_with='@funilrys').replace().replace('@funilrys', '')