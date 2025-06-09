def domain_name_left_cuts(domain):
    """returns a list of strings created by splitting the domain on
    '.' and successively cutting off the left most portion
    """
    cuts = []
    if domain:
        parts = domain.split('.')
        for i in range(len(parts)):
            cuts.append('.'.join(parts[i:]))
    return cuts