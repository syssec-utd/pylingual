def data_download(self, files):
    """Create the rst string to download supplementary data"""
    if len(files) > 1:
        return self.DATA_DOWNLOAD % ('\n\n' + ' ' * 8 + ('\n' + ' ' * 8).join(('* :download:`%s`' % f for f in files)))
    return self.DATA_DOWNLOAD % ':download:`%s`' % files[0]