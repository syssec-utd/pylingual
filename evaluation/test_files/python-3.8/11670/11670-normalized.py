def parse_mim_titles(lines):
    """Parse the mimTitles.txt file
    
    This file hold information about the description for each entry in omim.
    There is not information about entry type.
    parse_mim_titles collects the preferred title and maps it to the mim number.
    
    Args:
        lines(iterable): lines from mimTitles file
    
    Yields:
        parsed_entry(dict)
    
        {
        'mim_number': int, # The mim number for entry
        'preferred_title': str, # the preferred title for a entry
        }

    """
    header = ['prefix', 'mim_number', 'preferred_title', 'alternative_title', 'included_title']
    for (i, line) in enumerate(lines):
        line = line.rstrip()
        if not line.startswith('#'):
            parsed_entry = parse_omim_line(line, header)
            parsed_entry['mim_number'] = int(parsed_entry['mim_number'])
            parsed_entry['preferred_title'] = parsed_entry['preferred_title'].split(';')[0]
            yield parsed_entry