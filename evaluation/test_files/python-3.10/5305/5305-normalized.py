def message(msg, *args):
    """Program message output."""
    clear_progress()
    text = msg % args
    sys.stdout.write(text + '\n')