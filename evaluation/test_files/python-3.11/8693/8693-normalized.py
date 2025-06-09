def get_email_addresses(self):
    """
        : returns: dict of type and email address list
        :rtype: dict(str, list(str))
        """
    email_dict = {}
    for child in self.vcard.getChildren():
        if child.name == 'EMAIL':
            type = helpers.list_to_string(self._get_types_for_vcard_object(child, 'internet'), ', ')
            if type not in email_dict:
                email_dict[type] = []
            email_dict[type].append(child.value)
    for email_list in email_dict.values():
        email_list.sort()
    return email_dict