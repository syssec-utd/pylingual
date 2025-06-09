import threading
from datetime import datetime, timedelta
from time import sleep

class NumerousLogHandler:

    def __init__(self, client, admin_log_id=None, echo=False):
        self.client = client
        self.buffered_records = []
        self._buffer_lock = threading.Lock()
        self.last_push = datetime.utcnow() - timedelta(hours=1)
        self.debounce = 5
        self.admin_log_id = admin_log_id
        self.echo = echo
        self.stop_timed_flush = threading.Event()

        def timed_flush(stop_event: threading.Event):
            while not stop_event.is_set():
                now_ = datetime.utcnow()
                if (now_ - self.last_push).seconds > self.debounce:
                    self.last_push = now_
                    self.flush()
                sleep(1)
        threading.Thread(target=timed_flush, args=(self.stop_timed_flush,), daemon=True).start()

    def handle(self, record):
        self.log(record.msg)

    def log(self, message):
        now_ = datetime.utcnow()
        record = (now_, message)
        with self._buffer_lock:
            self.buffered_records.append(record)
        if self.echo:
            print(record)

    def flush(self):
        to_push = None
        with self._buffer_lock:
            if len(self.buffered_records) > 0:
                to_push = self.buffered_records.copy()
                self.buffered_records = []
        if to_push:
            if self.admin_log_id is not None:
                self.client.push_scenario_logs_admin(to_push, exe_id=self.admin_log_id)
            else:
                self.client.push_scenario_logs(to_push)

    def close(self):
        self.stop_timed_flush.set()
        self.flush()