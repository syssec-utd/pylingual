def _update_from_raw_data(self, raw_data, data_type_id=None, name=None, description=None):
    """
        Upload already serialized raw data and replace the existing dataset.

        Parameters
        ----------
        raw_data: bytes
            Dataset contents to upload.
        data_type_id : str
            Serialization format of the raw data.
            If None, the format of the existing dataset is used.
            Supported formats are:
                'PlainText'
                'GenericCSV'
                'GenericTSV'
                'GenericCSVNoHeader'
                'GenericTSVNoHeader'
                'ARFF'
            See the azureml.DataTypeIds class for constants.
        name : str, optional
            Name for the dataset.
            If None, the name of the existing dataset is used.
        description : str, optional
            Description for the dataset.
            If None, the name of the existing dataset is used.
        """
    _not_none('raw_data', raw_data)
    if data_type_id is None:
        data_type_id = self.data_type_id
    if name is None:
        name = self.name
    if description is None:
        description = self.description
    self._upload_and_refresh(raw_data, data_type_id, name, description)