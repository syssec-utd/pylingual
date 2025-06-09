def remove_sandbox(parent_dir, dir_name):
    """
    This function is written to remove sandbox directories if they exist under the
    parent_dir.

    :param parent_dir: string denoting full parent directory path
    :param dir_name: string denoting directory path which could be a sandbox
    :return: None
    """
    if 'Rsandbox' in dir_name:
        rsandbox_dir = os.path.join(parent_dir, dir_name)
        try:
            if sys.platform == 'win32':
                os.system('C:/cygwin64/bin/rm.exe -r -f "{0}"'.format(rsandbox_dir))
            else:
                shutil.rmtree(rsandbox_dir)
        except OSError as e:
            print('')
            print('ERROR: Removing RSandbox directory failed: ' + rsandbox_dir)
            print('       (errno {0}): {1}'.format(e.errno, e.strerror))
            print('')
            sys.exit(1)