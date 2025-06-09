def parse_peddy_ped_check(lines):
    """Parse a .ped_check.csv file
    
    Args:
        lines(iterable(str))
    
    Returns:
        ped_check(list(dict))
    """
    ped_check = []
    header = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if i == 0:
            header = line.lstrip('#').split(',')
        else:
            pair_info = dict(zip(header, line.split(',')))
            pair_info['hets_a'] = convert_number(pair_info['hets_a'])
            pair_info['hets_b'] = convert_number(pair_info['hets_b'])
            pair_info['ibs0'] = convert_number(pair_info['ibs0'])
            pair_info['ibs2'] = convert_number(pair_info['ibs2'])
            pair_info['n'] = convert_number(pair_info['n'])
            pair_info['rel'] = convert_number(pair_info['rel'])
            pair_info['pedigree_relatedness'] = convert_number(pair_info['pedigree_relatedness'])
            pair_info['rel_difference'] = convert_number(pair_info['rel_difference'])
            pair_info['shared_hets'] = convert_number(pair_info['shared_hets'])
            pair_info['pedigree_parents'] = make_bool(pair_info.get('pedigree_parents'))
            pair_info['predicted_parents'] = make_bool(pair_info.get('predicted_parents'))
            pair_info['parent_error'] = make_bool(pair_info.get('parent_error'))
            pair_info['sample_duplication_error'] = make_bool(pair_info.get('sample_duplication_error'))
            ped_check.append(pair_info)
    return ped_check