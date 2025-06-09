def _recursive_terminate_without_psutil(process):
    """Terminate a process and its descendants.
    """
    try:
        _recursive_terminate(process.pid)
    except OSError as e:
        warnings.warn('Failed to kill subprocesses on this platform. Pleaseinstall psutil: https://github.com/giampaolo/psutil')
        process.terminate()
    process.join()