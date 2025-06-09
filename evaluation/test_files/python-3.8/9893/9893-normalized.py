def __create_user_config(self):
    """ Copy the config template into user's directory """
    src_path = self.__get_config_template_path()
    src = os.path.abspath(src_path)
    if not os.path.exists(src):
        message = f'Config template not found {src}'
        self.logger.error(message)
        raise FileNotFoundError(message)
    dst = os.path.abspath(self.get_config_path())
    shutil.copyfile(src, dst)
    if not os.path.exists(dst):
        raise FileNotFoundError('Config file could not be copied to user dir!')