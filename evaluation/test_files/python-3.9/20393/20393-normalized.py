def get_readline_tail(self, n=10):
    """Get the last n items in readline history."""
    end = self.shell.readline.get_current_history_length() + 1
    start = max(end - n, 1)
    ghi = self.shell.readline.get_history_item
    return [ghi(x) for x in range(start, end)]