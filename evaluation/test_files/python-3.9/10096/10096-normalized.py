def create_metadata_tar(self, destination=None, metadata_folder='.singularity.d'):
    """create a metadata tar (runscript and environment) to add to the
       downloaded image. This function uses all functions in this section
       to obtain key--> values from the manifest config, and write
       to a .tar.gz

       Parameters
       ==========
       metadata_folder: the metadata folder in the singularity image.
                        default is .singularity.d
    """
    tar_file = None
    files = []
    environ = self._extract_env()
    if environ not in [None, '']:
        bot.verbose3('Adding Docker environment to metadata tar')
        template = get_template('tarinfo')
        template['name'] = './%s/env/10-docker.sh' % metadata_folder
        template['content'] = environ
        files.append(template)
    labels = self._extract_labels()
    if labels is not None:
        labels = print_json(labels)
        bot.verbose3('Adding Docker labels to metadata tar')
        template = get_template('tarinfo')
        template['name'] = './%s/labels.json' % metadata_folder
        template['content'] = labels
        files.append(template)
    runscript = self._extract_runscript()
    if runscript is not None:
        bot.verbose3('Adding Docker runscript to metadata tar')
        template = get_template('tarinfo')
        template['name'] = './%s/runscript' % metadata_folder
        template['content'] = runscript
        files.append(template)
    if len(files) > 0:
        dest = self._get_download_cache(destination, subfolder='metadata')
        tar_file = create_tar(files, dest)
    else:
        bot.warning('No metadata will be included.')
    return tar_file