def is_important_traceback(self, important_module, tb):
    """Walks a traceback's frames and checks if any of the frames
        originated in the given important module.  If that is the case then we
        were able to import the module itself but apparently something went
        wrong when the module was imported.  (Eg: import of an import failed).
        """
    while tb is not None:
        if self.is_important_frame(important_module, tb):
            return True
        tb = tb.tb_next
    return False