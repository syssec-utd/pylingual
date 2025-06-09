def derive_key(self, master_password):
    """ Computes the key from the salt and the master password. """
    encoder = encoding.Encoder(self.charset)
    bytes = ('%s:%s' % (master_password, self.name)).encode('utf8')
    start_time = time.clock()
    digest = scrypt.hash(bytes, self.salt, N=1 << 14, r=8, p=1)
    key = encoder.encode(digest, self.key_length)
    derivation_time_in_s = time.clock() - start_time
    _logger.debug('Key derivation took %.2fms', derivation_time_in_s * 1000)
    return key