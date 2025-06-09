def parse_files(self, fls):
    """Public method for parsing abricate output files.

        This method is called at at class instantiation for the provided
        output files. Additional abricate output files can be added using
        this method after the class instantiation.

        Parameters
        ----------
        fls : list
            List of paths to Abricate files

        """
    for f in fls:
        if os.path.exists(f):
            self._parser(f)
        else:
            logger.warning('File {} does not exist'.format(f))