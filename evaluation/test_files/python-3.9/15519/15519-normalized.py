def _redirect(self, stream, target):
    """Redirect a system stream to the provided target."""
    if target is None:
        target_fd = os.open(os.devnull, os.O_RDWR)
    else:
        target_fd = target.fileno()
    os.dup2(target_fd, stream.fileno())