def hierarchical(cls, element):
    """
        The idea behind this method is to sort a list of domain hierarchicaly.

        :param element: The element we are currently reading.
        :type element: str

        :return: The formatted element.
        :rtype: str

        .. note::
            For a domain like :code:`aaa.bbb.ccc.tdl`.

            A normal sorting is done in the following order:
                1. :code:`aaa`
                2. :code:`bbb`
                3. :code:`ccc`
                4. :code:`tdl`

            This method allow the sorting to be done in the following order:
                1. :code:`tdl`
                2. :code:`ccc`
                3. :code:`bbb`
                4. :code:`aaa`

        """
    to_sort = ''
    full_extension = ''
    element = element.lower()
    url_base = Check().is_url_valid(element, return_base=True)
    if not isinstance(url_base, str):
        if '.' in element:
            extension_index = element.rindex('.') + 1
            extension = element[extension_index:]
            if extension in PyFunceble.INTERN['psl_db']:
                for suffix in PyFunceble.INTERN['psl_db'][extension]:
                    formatted_suffix = '.' + suffix
                    if element.endswith(formatted_suffix):
                        suffix_index = element.rindex(formatted_suffix)
                        to_sort = element[:suffix_index]
                        full_extension = suffix
                        break
            if not full_extension:
                full_extension = element[extension_index:]
                to_sort = element[:extension_index - 1]
            full_extension += '.'
            tros_ot = to_sort[::-1]
            if '.' in tros_ot:
                full_extension = tros_ot[:tros_ot.index('.')][::-1] + '.' + full_extension
                tros_ot = tros_ot[tros_ot.index('.') + 1:]
                reversion = full_extension + '.'.join([x[::-1] for x in tros_ot.split('.')])
                return Regex(reversion, cls.regex_replace, replace_with='@funilrys').replace().replace('@funilrys', '')
            return Regex(to_sort + full_extension, cls.regex_replace, replace_with='@funilrys').replace().replace('@funilrys', '')
        return element
    protocol_position = element.rindex(url_base)
    protocol = element[:protocol_position]
    return protocol + cls.hierarchical(url_base)