def write_tokens_to_file(self):
    """ Write api tokens to a file """
    config = dict()
    config['API_KEY'] = self.api_key
    config['ACCESS_TOKEN'] = self.access_token
    config['REFRESH_TOKEN'] = self.refresh_token
    config['AUTHORIZATION_CODE'] = self.authorization_code
    if self.file_based_config:
        config_from_file(self.config_filename, config)
    else:
        self.config = config