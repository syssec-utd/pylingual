def get_win_launcher(type):
    """
    Load the Windows launcher (executable) suitable for launching a script.

    `type` should be either 'cli' or 'gui'

    Returns the executable as a byte string.
    """
    launcher_fn = '%s.exe' % type
    if platform.machine().lower() == 'arm':
        launcher_fn = launcher_fn.replace('.', '-arm.')
    if is_64bit():
        launcher_fn = launcher_fn.replace('.', '-64.')
    else:
        launcher_fn = launcher_fn.replace('.', '-32.')
    return resource_string('setuptools', launcher_fn)