def run(self, args):
    """Run a frame command. This routine is a little complex
        because we allow a number parameter variations."""
    if len(args) == 1:
        position_str = '0'
    elif len(args) == 2:
        name_or_id = args[1]
        frame, thread_id = self.get_from_thread_name_or_id(name_or_id, False)
        if frame is None:
            position_str = name_or_id
        else:
            position_str = '0'
            self.find_and_set_debugged_frame(frame, thread_id)
            pass
    elif len(args) == 3:
        name_or_id = args[1]
        position_str = args[2]
        frame, thread_id = self.get_from_thread_name_or_id(name_or_id)
        if frame is None:
            return
        self.find_and_set_debugged_frame(frame, thread_id)
        pass
    self.one_arg_run(position_str)
    return False