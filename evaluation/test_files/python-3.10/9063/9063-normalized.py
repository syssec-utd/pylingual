def upload_file(filename, server, account, projname, language=None, username=None, password=None, append=False, stage=False, date_format=None):
    """
    Upload a file to Luminoso with the given account and project name.

    Given a file containing JSON, JSON stream, or CSV data, this verifies
    that we can successfully convert it to a JSON stream, then uploads that
    JSON stream.
    """
    stream = transcode_to_stream(filename, date_format)
    upload_stream(stream_json_lines(stream), server, account, projname, language=language, username=username, password=password, append=append, stage=stage)