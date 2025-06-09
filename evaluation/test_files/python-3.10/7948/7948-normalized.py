def all_dimensions_names(self):
    """ Returns all the dimensions names, including the names of sub_fields
        and their corresponding packed fields
        """
    return frozenset(self.array.dtype.names + tuple(self.sub_fields_dict.keys()))