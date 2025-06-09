def finalize(self, result):
    """Clean up stats file, if configured to do so.
        """
    if not self.available():
        return
    try:
        self.prof.close()
    except AttributeError:
        pass
    if self.clean_stats_file:
        if self.fileno:
            try:
                os.close(self.fileno)
            except OSError:
                pass
        try:
            os.unlink(self.pfile)
        except OSError:
            pass
    return None