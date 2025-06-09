def lines_without_stdlib(self):
    """Filters code from standard library from self.lines."""
    prev_line = None
    current_module_path = inspect.getabsfile(inspect.currentframe())
    for module_path, lineno, runtime in self.lines:
        module_abspath = os.path.abspath(module_path)
        if not prev_line:
            prev_line = [module_abspath, lineno, runtime]
        elif not check_standard_dir(module_path) and module_abspath != current_module_path:
            yield prev_line
            prev_line = [module_abspath, lineno, runtime]
        else:
            prev_line[2] += runtime
    yield prev_line