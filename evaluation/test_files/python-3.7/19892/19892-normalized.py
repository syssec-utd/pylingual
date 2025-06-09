def delete_index(self):
    """Deletes the underlying ES index.

        Only use this if you know what you're doing. This destroys
        the entire underlying ES index, which could be shared by
        multiple distinct ElasticStore instances.
        """
    if self.conn.indices.exists(index=self.index):
        self.conn.indices.delete(index=self.index)