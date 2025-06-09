def _extract_record(self, rec):
    """decompose a TaskRecord dict into subsection of reply for get_result"""
    io_dict = {}
    for key in ('pyin', 'pyout', 'pyerr', 'stdout', 'stderr'):
        io_dict[key] = rec[key]
    content = {'result_content': rec['result_content'], 'header': rec['header'], 'result_header': rec['result_header'], 'received': rec['received'], 'io': io_dict}
    if rec['result_buffers']:
        buffers = map(bytes, rec['result_buffers'])
    else:
        buffers = []
    return (content, buffers)