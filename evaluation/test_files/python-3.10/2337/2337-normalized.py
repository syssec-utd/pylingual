def update_message_dict(message_dict, action):
    """
    Update the g_ok_java_messages dict structure by
    1. add the new java ignored messages stored in message_dict if action == 1
    2. remove the java ignored messages stired in message_dict if action == 2.

    Parameters
    ----------

    message_dict :  Python dict
      key: unit test name or "general"
      value: list of java messages that are to be ignored if they are found when running the test stored as the key.  If
        the key is "general", the list of java messages are to be ignored when running all tests.
    action : int
      if 1: add java ignored messages stored in message_dict to g_ok_java_messages dict;
      if 2: remove java ignored messages stored in message_dict from g_ok_java_messages dict.

    :return: none
    """
    global g_ok_java_messages
    allKeys = g_ok_java_messages.keys()
    for key in message_dict.keys():
        if key in allKeys:
            for message in message_dict[key]:
                if action == 1:
                    if message not in g_ok_java_messages[key]:
                        g_ok_java_messages[key].append(message)
                if action == 2:
                    if message in g_ok_java_messages[key]:
                        g_ok_java_messages[key].remove(message)
        elif action == 1:
            g_ok_java_messages[key] = message_dict[key]