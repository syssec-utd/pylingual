def extract_tar(archive, output_folder, handle_whiteout=False):
    """extract a tar archive to a specified output folder

        Parameters
        ==========
        archive: the archive file to extract
        output_folder: the output folder to extract to
        handle_whiteout: use docker2oci variation to handle whiteout files

    """
    from .terminal import run_command
    if handle_whiteout is True:
        return _extract_tar(archive, output_folder)
    args = '-xf'
    if archive.endswith('.tar.gz'):
        args = '-xzf'
    command = ['tar', args, archive, '-C', output_folder, '--exclude=dev/*']
    if not bot.is_quiet():
        print('Extracting %s' % archive)
    return run_command(command)