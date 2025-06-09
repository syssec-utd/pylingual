def post_data(self, file_name=None, legacy=False, verifytype=VERIFY_BY_SLICE):
    """
        Arguments:
            file_name (str): The file name of the json file to post (optional).
                If this is left unspecified it is assumed the data is in the
                AutoIngest object.
            dev (bool): If pushing to a microns dev branch server set this
                to True, if not leave False.
            verifytype (enum): Set http verification type, by checking the
                first slice is accessible or by checking channel folder.
                NOTE: If verification occurs by folder there is NO image size
                or type verification. Enum: [Folder, Slice]

        Returns:
            None
        """
    if file_name is None:
        complete_example = (self.dataset, self.project, self.channels, self.metadata)
        data = json.loads(self.nd_json(*complete_example))
    else:
        try:
            with open(file_name) as data_file:
                data = json.load(data_file)
        except:
            raise OSError('Error opening file')
    self.put_data(data)