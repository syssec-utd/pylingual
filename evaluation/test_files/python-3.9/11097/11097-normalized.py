def user_config_file(self):
    """Get the absolute path to the user config file."""
    return os.path.join(get_user_config_dir(self.app_name, self.app_author), self.filename)