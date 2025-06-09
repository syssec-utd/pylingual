def transcode_to_stream(input_filename, date_format=None):
    """
    Read a JSON or CSV file and convert it into a JSON stream, which will
    be saved in an anonymous temp file.
    """
    tmp = tempfile.TemporaryFile()
    for entry in open_json_or_csv_somehow(input_filename, date_format=date_format):
        tmp.write(json.dumps(entry, ensure_ascii=False).encode('utf-8'))
        tmp.write(b'\n')
    tmp.seek(0)
    return tmp