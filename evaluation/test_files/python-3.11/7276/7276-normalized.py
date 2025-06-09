def add_from_raw_data(self, raw_data, data_type_id, name, description):
    """
        Upload already serialized raw data as a new dataset.

        Parameters
        ----------
        raw_data: bytes
            Dataset contents to upload.
        data_type_id : str
            Serialization format of the raw data.
            Supported formats are:
                'PlainText'
                'GenericCSV'
                'GenericTSV'
                'GenericCSVNoHeader'
                'GenericTSVNoHeader'
                'ARFF'
            See the azureml.DataTypeIds class for constants.
        name : str
            Name for the new dataset.
        description : str
            Description for the new dataset.

        Returns
        -------
        SourceDataset
            Dataset that was just created.
            Use open(), read_as_binary(), read_as_text() or to_dataframe() on
            the dataset object to get its contents as a stream, bytes, str or
            pandas DataFrame.
        """
    _not_none('raw_data', raw_data)
    _not_none_or_empty('data_type_id', data_type_id)
    _not_none_or_empty('name', name)
    _not_none_or_empty('description', description)
    return self._upload(raw_data, data_type_id, name, description)