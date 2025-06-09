def setMeterPassword(self, new_pwd, pwd='00000000'):
    """ Serial Call to set meter password.  USE WITH CAUTION.

        Args:
            new_pwd (str): 8 digit numeric password to set
            pwd (str): Old 8 digit numeric password.

        Returns:
            bool: True on completion with ACK.
        """
    result = False
    self.setContext('setMeterPassword')
    try:
        if len(new_pwd) != 8 or len(pwd) != 8:
            self.writeCmdMsg('Passwords must be exactly eight characters.')
            self.setContext('')
            return result
        if not self.request(False):
            self.writeCmdMsg('Pre command read failed: check serial line.')
        elif not self.serialCmdPwdAuth(pwd):
            self.writeCmdMsg('Password failure')
        else:
            req_pwd = binascii.hexlify(new_pwd.zfill(8))
            req_str = '015731023030323028' + req_pwd + '2903'
            req_str += self.calc_crc16(req_str[2:].decode('hex'))
            self.m_serial_port.write(req_str.decode('hex'))
            if self.m_serial_port.getResponse(self.getContext()).encode('hex') == '06':
                self.writeCmdMsg('Success(setMeterPassword): 06 returned.')
                result = True
        self.serialPostEnd()
    except:
        ekm_log(traceback.format_exc(sys.exc_info()))
    self.setContext('')
    return result