def handshake(self, protocol='vnc', width=1024, height=768, dpi=96, audio=None, video=None, image=None, **kwargs):
    """
        Establish connection with Guacamole guacd server via handshake.
        """
    if protocol not in PROTOCOLS:
        self.logger.debug('Invalid protocol: %s' % protocol)
        raise GuacamoleError('Cannot start Handshake. Missing protocol.')
    if audio is None:
        audio = list()
    if video is None:
        video = list()
    if image is None:
        image = list()
    self.logger.debug('Send `select` instruction.')
    self.send_instruction(Instruction('select', protocol))
    instruction = self.read_instruction()
    self.logger.debug('Expecting `args` instruction, received: %s' % str(instruction))
    if not instruction:
        self.close()
        raise GuacamoleError('Cannot establish Handshake. Connection Lost!')
    if instruction.opcode != 'args':
        self.close()
        raise GuacamoleError('Cannot establish Handshake. Expected opcode `args`, received `%s` instead.' % instruction.opcode)
    self.logger.debug('Send `size` instruction (%s, %s, %s)' % (width, height, dpi))
    self.send_instruction(Instruction('size', width, height, dpi))
    self.logger.debug('Send `audio` instruction (%s)' % audio)
    self.send_instruction(Instruction('audio', *audio))
    self.logger.debug('Send `video` instruction (%s)' % video)
    self.send_instruction(Instruction('video', *video))
    self.logger.debug('Send `image` instruction (%s)' % image)
    self.send_instruction(Instruction('image', *image))
    connection_args = [kwargs.get(arg.replace('-', '_'), '') for arg in instruction.args]
    self.logger.debug('Send `connect` instruction (%s)' % connection_args)
    self.send_instruction(Instruction('connect', *connection_args))
    instruction = self.read_instruction()
    self.logger.debug('Expecting `ready` instruction, received: %s' % str(instruction))
    if instruction.opcode != 'ready':
        self.logger.warning('Expected `ready` instruction, received: %s instead')
    if instruction.args:
        self._id = instruction.args[0]
        self.logger.debug('Established connection with client id: %s' % self.id)
    self.logger.debug('Handshake completed.')
    self.connected = True