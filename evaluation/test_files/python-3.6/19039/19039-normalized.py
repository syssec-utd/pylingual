def files(text):
    """
    Iterate over <FILENAME> XML-like tags and tokenize with nltk
    """
    for f_match in filename_re.finditer(text):
        yield (f_match.group('stream_id'), f_match.group('tagged_doc'))