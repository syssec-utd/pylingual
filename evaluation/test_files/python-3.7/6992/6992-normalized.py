def unused_import_module_name(messages):
    """Yield line number and module name of unused imports."""
    pattern = "\\'(.+?)\\'"
    for message in messages:
        if isinstance(message, pyflakes.messages.UnusedImport):
            module_name = re.search(pattern, str(message))
            module_name = module_name.group()[1:-1]
            if module_name:
                yield (message.lineno, module_name)