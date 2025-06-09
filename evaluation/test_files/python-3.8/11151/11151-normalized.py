def getSessionInfo(self):
    """
        C_GetSessionInfo

        :return: a :class:`CK_SESSION_INFO` object
        """
    sessioninfo = PyKCS11.LowLevel.CK_SESSION_INFO()
    rv = self.lib.C_GetSessionInfo(self.session, sessioninfo)
    if rv != CKR_OK:
        raise PyKCS11Error(rv)
    s = CK_SESSION_INFO()
    s.slotID = sessioninfo.slotID
    s.state = sessioninfo.state
    s.flags = sessioninfo.flags
    s.ulDeviceError = sessioninfo.ulDeviceError
    return s