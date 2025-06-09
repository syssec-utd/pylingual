def parse_pipeline(pipeline_str):
    """Parses a pipeline string into a list of dictionaries with the connections
     between processes

    Parameters
    ----------
    pipeline_str : str
        String with the definition of the pipeline, e.g.::
            'processA processB processC(ProcessD | ProcessE)'

    Returns
    -------
    pipeline_links : list

    """
    if os.path.exists(pipeline_str):
        logger.debug('Found pipeline file: {}'.format(pipeline_str))
        with open(pipeline_str) as fh:
            pipeline_str = ''.join([x.strip() for x in fh.readlines()])
    logger.info(colored_print('Resulting pipeline string:\n'))
    logger.info(colored_print(pipeline_str + '\n'))
    insanity_checks(pipeline_str)
    logger.debug('Parsing pipeline string: {}'.format(pipeline_str))
    pipeline_links = []
    lane = 1
    (pipeline_str_modified, identifiers_to_tags) = add_unique_identifiers(pipeline_str)
    nforks = pipeline_str_modified.count(FORK_TOKEN)
    logger.debug('Found {} fork(s)'.format(nforks))
    if not nforks:
        logger.debug('Detected linear pipeline string : {}'.format(pipeline_str))
        linear_pipeline = ['__init__'] + pipeline_str_modified.split()
        pipeline_links.extend(linear_connection(linear_pipeline, lane))
        pipeline_links = remove_unique_identifiers(identifiers_to_tags, pipeline_links)
        return pipeline_links
    for i in range(nforks):
        logger.debug('Processing fork {} in lane {}'.format(i, lane))
        fields = pipeline_str_modified.split(FORK_TOKEN, i + 1)
        previous_process = fields[-2].split(LANE_TOKEN)[-1].split()
        logger.debug('Previous processes string: {}'.format(fields[-2]))
        logger.debug('Previous processes list: {}'.format(previous_process))
        next_lanes = get_lanes(fields[-1])
        logger.debug('Next lanes object: {}'.format(next_lanes))
        fork_sink = [x[0] for x in next_lanes]
        logger.debug('The fork sinks into the processes: {}'.format(fork_sink))
        if i == 0:
            if not previous_process:
                previous_process = ['__init__']
                lane = 0
            else:
                previous_process = ['__init__'] + previous_process
            pipeline_links.extend(linear_connection(previous_process, lane))
        fork_source = previous_process[-1]
        logger.debug('Fork source is set to: {}'.format(fork_source))
        fork_lane = get_source_lane(previous_process, pipeline_links)
        logger.debug('Fork lane is set to: {}'.format(fork_lane))
        pipeline_links.extend(fork_connection(fork_source, fork_sink, fork_lane, lane))
        pipeline_links.extend(linear_lane_connection(next_lanes, lane))
        lane += len(fork_sink)
    pipeline_links = remove_unique_identifiers(identifiers_to_tags, pipeline_links)
    return pipeline_links