def write_quick(self, addr):
    """write_quick(addr)

        Perform SMBus Quick transaction.
        """
    self._set_addr(addr)
    if SMBUS.i2c_smbus_write_quick(self._fd, SMBUS.I2C_SMBUS_WRITE) != 0:
        raise IOError(ffi.errno)