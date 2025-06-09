def block_process_call(self, addr, cmd, vals):
    """block_process_call(addr, cmd, vals) -> results

        Perform SMBus Block Process Call transaction.
        """
    self._set_addr(addr)
    data = ffi.new('union i2c_smbus_data *')
    list_to_smbus_data(data, vals)
    if SMBUS.i2c_smbus_access(self._fd, SMBUS.I2C_SMBUS_WRITE, ffi.cast('__u8', cmd), SMBUS.I2C_SMBUS_BLOCK_PROC_CALL, data):
        raise IOError(ffi.errno)
    return smbus_data_to_list(data)