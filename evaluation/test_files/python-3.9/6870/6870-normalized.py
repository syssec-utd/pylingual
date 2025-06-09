def handle(cls, status, invalid_source='IANA'):
    """
        Handle the lack of WHOIS and expiration date. :smile_cat:

        :param matched_status: The status that we have to handle.
        :type status: str

        :param invalid_source:
            The source to set when we handle INVALID element.
        :type invalid_source: str

        :return:
            The strus of the domain after generating the files desired
            by the user.
        :rtype: str
        """
    if status.lower() not in PyFunceble.STATUS['list']['invalid']:
        source = 'NSLOOKUP'
        if Lookup().nslookup():
            (status, source) = cls.extra_rules.handle(PyFunceble.STATUS['official']['up'], source)
            Generate(status, source).status_file()
            return (status, source)
        (status, source) = cls.extra_rules.handle(PyFunceble.STATUS['official']['down'], source)
        Generate(status, source).status_file()
        return (status, source)
    (status, source) = cls.extra_rules.handle(PyFunceble.STATUS['official']['invalid'], invalid_source)
    Generate(status, source).status_file()
    return (status, source)