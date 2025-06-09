def delete_all_checkpoints(self, path):
    """Delete all checkpoints for the given path."""
    with self.engine.begin() as db:
        delete_remote_checkpoints(db, self.user_id, path)