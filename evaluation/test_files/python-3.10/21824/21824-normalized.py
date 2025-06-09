def get_versioned_files():
    """List all files versioned by git in the current directory."""
    encoding = 'UTF-8' if sys.platform == 'win32' else None
    output = run(['git', 'ls-files', '-z'], encoding=encoding)
    return add_directories(output.split('\x00')[:-1])