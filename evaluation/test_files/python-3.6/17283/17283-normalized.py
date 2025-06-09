def dumps(obj):
    """
    Serializes a dictionary into Manifest data.
    :param obj: A dictionary to serialize.
    :return: A file object.
    """
    if not isinstance(obj, dict):
        raise TypeError('can only dump a dictionary as a Manifest but got ' + type(obj).__name__)
    data = []
    int32 = struct.Struct('<I')
    for message_name in ('payload', 'metadata', 'signature'):
        message_data = obj[message_name]
        message_id = MSG_IDS[message_name]
        message_class = MessageClass[message_id]
        message = dict_to_protobuf(message_class, message_data)
        message_bytes = message.SerializeToString()
        message_size = len(message_bytes)
        data.append(int32.pack(message_id))
        data.append(int32.pack(message_size))
        data.append(message_bytes)
    data.append(int32.pack(MSG_EOF))
    return b''.join(data)