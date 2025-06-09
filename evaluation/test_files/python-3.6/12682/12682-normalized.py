def _prm_read_dictionary(self, leaf, full_name):
    """Loads data that was originally a dictionary when stored

        :param leaf:

            PyTables table containing the dictionary data

        :param full_name:

            Full name of the parameter or result whose data is to be loaded

        :return:

            Data to be loaded

        """
    try:
        temp_table = self._prm_read_table(leaf, full_name)
        temp_dict = temp_table.to_dict('list')
        innder_dict = {}
        for (innerkey, vallist) in temp_dict.items():
            innder_dict[innerkey] = vallist[0]
        return innder_dict
    except:
        self._logger.error('Failed loading `%s` of `%s`.' % (leaf._v_name, full_name))
        raise