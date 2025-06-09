def messages(location, receiver):
    """Construct a function that checks a directory for messages

    The function checks for new messages and
    calls the appropriate method on the receiver. Sent messages are
    deleted.

    :param location: string, the directory to monitor
    :param receiver: IEventReceiver
    :returns: a function with no parameters
    """
    path = filepath.FilePath(location)

    def _check(path):
        messageFiles = path.globChildren('*')
        for message in messageFiles:
            if message.basename().endswith('.new'):
                continue
            receiver.message(message.getContent())
            message.remove()
    return functools.partial(_check, path)