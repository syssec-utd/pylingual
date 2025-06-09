def read_entry(self, file_name):
    """
        Args:
            file_name (str):

        Returns:
            pd.DataFrame:
        """
    file_path = os.path.join(self.EXTRACTION_CACHE_PATH, file_name)
    logger.info(f'Reading cache entry: {file_path}')
    return joblib.load(file_path)