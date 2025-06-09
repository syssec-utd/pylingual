def delete_all(self):
    """Deletes all storage.

        This includes every content object and all index data.
        """
    self.kvl.clear_table(self.TABLE)
    self.kvl.clear_table(self.INDEX_TABLE)