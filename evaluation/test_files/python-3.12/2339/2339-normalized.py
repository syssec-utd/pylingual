def add_to_dict(val, key, message_dict):
    """
    Add new key, val (ignored java message) to dict message_dict.

    Parameters
    ----------

    val :  Str
       contains ignored java messages.
    key :  Str
        key for the ignored java messages.  It can be "general" or any R or Python unit
        test names
    message_dict :  dict
        stored ignored java message for key ("general" or any R or Python unit test names)

    :return: none
    """
    allKeys = message_dict.keys()
    if len(val) > 0:
        if key in allKeys and val not in message_dict[key]:
            message_dict[key].append(val)
        else:
            message_dict[key] = [val]