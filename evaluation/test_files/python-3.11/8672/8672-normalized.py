def email_subcommand(search_terms, vcard_list, parsable, remove_first_line):
    """Print a mail client friendly contacts table that is compatible with the
    default format used by mutt.
    Output format:
        single line of text
        email_address	name	type
        email_address	name	type
        [...]

    :param search_terms: used as search term to filter the contacts before
        printing
    :type search_terms: str
    :param vcard_list: the vcards to search for matching entries which should
        be printed
    :type vcard_list: list of carddav_object.CarddavObject
    :param parsable: machine readable output: columns devided by tabulator (	)
    :type parsable: bool
    :param remove_first_line: remove first line (searching for '' ...)
    :type remove_first_line: bool
    :returns: None
    :rtype: None

    """
    matching_email_address_list = []
    all_email_address_list = []
    for vcard in vcard_list:
        for type, email_list in sorted(vcard.get_email_addresses().items(), key=lambda k: k[0].lower()):
            for email in sorted(email_list):
                if config.display_by_name() == 'first_name':
                    name = vcard.get_first_name_last_name()
                else:
                    name = vcard.get_last_name_first_name()
                line_formatted = '\t'.join([name, type, email])
                line_parsable = '\t'.join([email, name, type])
                if parsable:
                    email_address_line = line_parsable
                else:
                    email_address_line = line_formatted
                if re.search(search_terms, '%s\n%s' % (line_formatted, line_parsable), re.IGNORECASE | re.DOTALL):
                    matching_email_address_list.append(email_address_line)
                all_email_address_list.append(email_address_line)
    if matching_email_address_list:
        if parsable:
            if not remove_first_line:
                print("searching for '%s' ..." % search_terms)
            print('\n'.join(matching_email_address_list))
        else:
            list_email_addresses(matching_email_address_list)
    elif all_email_address_list:
        if parsable:
            if not remove_first_line:
                print("searching for '%s' ..." % search_terms)
            print('\n'.join(all_email_address_list))
        else:
            list_email_addresses(all_email_address_list)
    else:
        if not parsable:
            print('Found no email addresses')
        elif not remove_first_line:
            print("searching for '%s' ..." % search_terms)
        sys.exit(1)