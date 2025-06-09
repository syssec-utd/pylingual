def omim_terms(case_obj):
    """Extract all OMIM phenotypes available for the case
    Args:
        case_obj(dict): a scout case object
    Returns:
        disorders(list): a list of OMIM disorder objects
    """
    LOG.info('Collecting OMIM disorders for case {}'.format(case_obj.get('display_name')))
    disorders = []
    case_disorders = case_obj.get('diagnosis_phenotypes')
    if case_disorders:
        for disorder in case_disorders:
            disorder_obj = {'id': ':'.join(['MIM', str(disorder)])}
            disorders.append(disorder_obj)
    return disorders