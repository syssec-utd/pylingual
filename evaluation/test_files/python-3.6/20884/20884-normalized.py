def _exit_now_changed(self, name, old, new):
    """stop eventloop when exit_now fires"""
    if new:
        loop = ioloop.IOLoop.instance()
        loop.add_timeout(time.time() + 0.1, loop.stop)