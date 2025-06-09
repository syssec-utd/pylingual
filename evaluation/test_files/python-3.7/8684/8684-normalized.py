def from_user_input(cls, address_book, user_input, supported_private_objects, version, localize_dates):
    """Use this if you want to create a new contact from user input."""
    contact = cls(address_book, None, supported_private_objects, version, localize_dates)
    contact._process_user_input(user_input)
    return contact