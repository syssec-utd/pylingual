def _create_app(self):
    """
        Method for creating a new Application Template.
        USAGE: cloud-harness create <dir_name> [--destination=<path>]
        """
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), self.TEMPLATE_FOLDER, self.TEMPLATE_FILENAME)
    new_dir = self._arguments['<dir_name>']
    override_destination = self._arguments.get('--destination', None)
    if override_destination is not None:
        if override_destination == '':
            raise ValueError('Destination path is empty')
        if os.path.isabs(override_destination) and os.path.isdir(override_destination):
            new_dir = os.path.join(override_destination, new_dir)
        else:
            override_path = os.path.join(os.getcwd(), override_destination)
            if not os.path.isabs(override_path) or not os.path.isdir(override_path):
                raise ValueError('New path parameter %s is not a directory' % override_destination)
            new_dir = os.path.join(override_path, new_dir)
    else:
        if os.path.isabs(new_dir) or os.path.sep in new_dir:
            raise ValueError('Directory name is invalid')
        new_dir = os.path.join(os.getcwd(), new_dir)
    os.makedirs(new_dir)
    new_file_path = os.path.join(new_dir, self.DEFAULT_NEW_APP_FILENAME)
    shutil.copyfile(template_path, new_file_path)
    printer('New Application created at %s' % new_file_path)