def start(self):
    """
        Parse the command line and start PyJFuzz
        """
    from .pjf_worker import PJFWorker
    worker = PJFWorker(self)
    if self.update_pjf:
        worker.update_library()
    elif self.browser_auto:
        worker.browser_autopwn()
    elif self.fuzz_web:
        worker.web_fuzzer()
    elif self.json:
        if not self.web_server and (not self.ext_fuzz) and (not self.cmd_fuzz):
            worker.fuzz()
        elif self.ext_fuzz:
            if self.stdin:
                worker.fuzz_stdin()
            else:
                worker.fuzz_command_line()
        elif self.cmd_fuzz:
            if self.stdin:
                worker.fuzz_external(True)
            else:
                worker.fuzz_external()
        else:
            worker.start_http_server()
    elif self.json_file:
        worker.start_file_fuzz()
    elif self.process_to_monitor:
        worker.start_process_monitor()