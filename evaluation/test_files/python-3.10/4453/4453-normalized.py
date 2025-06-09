def count_matched_codes(codes_regex, codes_dict):
    """ helper to aggregate codes by mask """
    total = 0
    for (code, count) in codes_dict.items():
        if codes_regex.match(str(code)):
            total += count
    return total