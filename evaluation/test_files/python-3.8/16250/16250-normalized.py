def export(self, location):
    """
        Export the Bazaar repository at the url to the destination location
        """
    temp_dir = tempfile.mkdtemp('-export', 'pip-')
    self.unpack(temp_dir)
    if os.path.exists(location):
        rmtree(location)
    try:
        self.run_command(['export', location], cwd=temp_dir, show_stdout=False)
    finally:
        rmtree(temp_dir)