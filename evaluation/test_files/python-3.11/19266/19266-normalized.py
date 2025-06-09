def _send_message(self, msg):
    """Add message to queue and start processing the queue."""
    LWLink.the_queue.put_nowait(msg)
    if LWLink.thread is None or not LWLink.thread.isAlive():
        LWLink.thread = Thread(target=self._send_queue)
        LWLink.thread.start()