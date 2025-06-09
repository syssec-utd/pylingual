def error(self, session=None):
    """
        Forces the task instance's state to FAILED in the database.
        """
    self.log.error('Recording the task instance as FAILED')
    self.state = State.FAILED
    session.merge(self)
    session.commit()