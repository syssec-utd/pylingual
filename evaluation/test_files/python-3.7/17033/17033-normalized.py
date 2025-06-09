def mech_from_string(input_string):
    """
        Takes a string form of a mechanism OID, in dot-separated: "1.2.840.113554.1.2.2" or numeric
        ASN.1: "{1 2 840 113554 1 2 2}" notation, and returns an :class:`OID` object representing
        the mechanism, which can be passed to other GSSAPI methods.

        :param input_string: a string representing the desired mechanism OID.
        :returns: the mechanism OID.
        :rtype: :class:`OID`
        :raises: ValueError if the the input string is ill-formatted.
        :raises: KeyError if the mechanism identified by the string is not supported by the
            underlying GSSAPI implementation.
        """
    if not re.match('^\\d+(\\.\\d+)*$', input_string):
        if re.match('^\\{\\d+( \\d+)*\\}$', input_string):
            input_string = '.'.join(input_string[1:-1].split())
        else:
            raise ValueError(input_string)
    for mech in get_all_mechs():
        if input_string == str(mech):
            return mech
    raise KeyError('Unknown mechanism: {0}'.format(input_string))