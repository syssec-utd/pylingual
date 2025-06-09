def terminate(self, exc_info=None):
    """Terminate all threads by deleting the queue and forcing the child threads
       to quit.
    """
    if exc_info:
        self.exc_info = exc_info
    try:
        while self.get_nowait():
            self.task_done()
    except Queue.Empty:
        pass