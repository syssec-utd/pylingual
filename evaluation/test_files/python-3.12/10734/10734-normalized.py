def get_results_file_name(boundaries_id, labels_id, config, annotator_id):
    """Based on the config and the dataset, get the file name to store the
    results."""
    utils.ensure_dir(msaf.config.results_dir)
    file_name = os.path.join(msaf.config.results_dir, 'results')
    file_name += '_boundsE%s_labelsE%s' % (boundaries_id, labels_id)
    file_name += '_annotatorE%d' % annotator_id
    sorted_keys = sorted(config.keys(), key=str.lower)
    for key in sorted_keys:
        file_name += '_%sE%s' % (key, str(config[key]).replace('/', '_'))
    if len(file_name) > 255 - len(msaf.config.results_ext):
        file_name = file_name[:255 - len(msaf.config.results_ext)]
    return file_name + msaf.config.results_ext