def duplicate_key_line_numbers(messages, source):
    """Yield line numbers of duplicate keys."""
    messages = [message for message in messages if isinstance(message, pyflakes.messages.MultiValueRepeatedKeyLiteral)]
    if messages:
        key_to_messages = create_key_to_messages_dict(messages)
        lines = source.split('\n')
        for (key, messages) in key_to_messages.items():
            good = True
            for message in messages:
                line = lines[message.lineno - 1]
                key = message.message_args[0]
                if not dict_entry_has_key(line, key):
                    good = False
            if good:
                for message in messages:
                    yield message.lineno