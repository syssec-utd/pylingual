def uncompressed(self):
    """If true, handle uncompressed data
        """
    ISUNCOMPRESSED = self.verboseRead(BoolCode('UNCMPR', description='Is uncompressed?'))
    if ISUNCOMPRESSED:
        self.verboseRead(FillerAlphabet(streamPos=self.stream.pos))
        print('Uncompressed data:')
        self.output += self.stream.readBytes(self.MLEN)
        print(outputFormatter(self.output[-self.MLEN:]))
    return ISUNCOMPRESSED