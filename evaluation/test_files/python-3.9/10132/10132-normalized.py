def get_uri(self):
    """generate a uri on the fly from database parameters if one is not
        saved with the initial model (it should be, but might not be possible)
        """
    uri = '%s/%s:%s' % (self.collection.name, self.name, self.tag)
    if self.version not in [None, '']:
        uri = '%s@%s' % (uri, self.version)
    return uri