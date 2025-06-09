def _wait(self):
    """Used for unittesting to make sure the plots are all done"""
    logger.debug('will wait for last plot to finish')
    self._plot_event = threading.Event()
    self.queue_update._wait()
    self.queue_replot._wait()
    self.queue_redraw._wait()
    qt_app = QtCore.QCoreApplication.instance()
    sleep = 10
    while not self._plot_event.is_set():
        logger.debug('waiting for last plot to finish')
        qt_app.processEvents()
        QtTest.QTest.qSleep(sleep)
    logger.debug('waiting for plot finished')