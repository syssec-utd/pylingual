def with_valid_checksum(self):
    """
        Returns the address with a valid checksum attached.
        """
    return Address(trytes=self.address + self._generate_checksum(), balance=self.balance, key_index=self.key_index, security_level=self.security_level)