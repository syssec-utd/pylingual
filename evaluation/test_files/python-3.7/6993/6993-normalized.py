def star_import_used_line_numbers(messages):
    """Yield line number of star import usage."""
    for message in messages:
        if isinstance(message, pyflakes.messages.ImportStarUsed):
            yield message.lineno