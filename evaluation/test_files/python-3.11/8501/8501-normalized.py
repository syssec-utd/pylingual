def decode(message):
    """
        The decoder understands the comma-seperated format produced by the encoder and
        allocates the two values to the correct keys:
            data['hello'] = 'world'
            data['x'] = 10

        """
    hello, x = message.payload.split(',')
    data = {}
    data['hello'] = hello
    data['x'] = x
    timestamp = datetime.now(pytz.timezone('UTC'))
    return Message(data, timestamp)