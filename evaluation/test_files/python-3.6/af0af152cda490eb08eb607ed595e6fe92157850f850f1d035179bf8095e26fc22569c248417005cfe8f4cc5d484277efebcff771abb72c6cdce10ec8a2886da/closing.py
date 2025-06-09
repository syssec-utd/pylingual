import signal

class Closing:
    closes = []

    @classmethod
    def add_close(cls, close: callable):
        cls.closes.append(close)

    @classmethod
    def close(cls):
        for close in cls.closes:
            close()
signal.signal(signal.SIGTERM, lambda *args: Closing.close())
signal.signal(signal.SIGINT, lambda *args: Closing.close())
signal.signal(signal.SIGILL, lambda *args: Closing.close())