def set_context(self, ti):
    """
        Provide task_instance context to airflow task handler.
        :param ti: task instance object
        """
    local_loc = self._init_file(ti)
    self.handler = logging.FileHandler(local_loc)
    self.handler.setFormatter(self.formatter)
    self.handler.setLevel(self.level)