def create_interrupt_event():
    """ Create an interrupt event handle.

        The parent process should use this static method for creating the
        interrupt event that is passed to the child process. It should store
        this handle and use it with ``send_interrupt`` to interrupt the child
        process.
        """

    class SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [('nLength', ctypes.c_int), ('lpSecurityDescriptor', ctypes.c_void_p), ('bInheritHandle', ctypes.c_int)]
    sa = SECURITY_ATTRIBUTES()
    sa_p = ctypes.pointer(sa)
    sa.nLength = ctypes.sizeof(SECURITY_ATTRIBUTES)
    sa.lpSecurityDescriptor = 0
    sa.bInheritHandle = 1
    return ctypes.windll.kernel32.CreateEventA(sa_p, False, False, '')