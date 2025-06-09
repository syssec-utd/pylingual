def send(self, request, **kwargs):
    """ Wraps a file, described in request, in a Response object.

            :param request: The PreparedRequest` being "sent".
            :returns: a Response object containing the file
        """
    if request.method not in ('GET', 'HEAD'):
        raise ValueError('Invalid request method %s' % request.method)
    url_parts = urlparse(request.url)
    if is_win32 and url_parts.netloc.endswith(':'):
        url_parts = url_parts._replace(path='/' + url_parts.netloc + url_parts.path, netloc='')
    if url_parts.netloc and url_parts.netloc not in ('localhost', '.', '..', '-'):
        raise ValueError('file: URLs with hostname components are not permitted')
    if url_parts.netloc in ('.', '..'):
        pwd = os.path.abspath(url_parts.netloc).replace(os.sep, '/') + '/'
        if is_win32:
            pwd = '/' + pwd
        url_parts = url_parts._replace(path=urljoin(pwd, url_parts.path.lstrip('/')))
    resp = Response()
    resp.url = request.url
    try:
        if url_parts.netloc == '-':
            if is_py3:
                resp.raw = sys.stdin.buffer
            else:
                resp.raw = sys.stdin
            resp.url = 'file://' + os.path.abspath('.').replace(os.sep, '/') + '/'
        else:
            path_parts = [unquote(p) for p in url_parts.path.split('/')]
            while path_parts and (not path_parts[0]):
                path_parts.pop(0)
            if any((os.sep in p for p in path_parts)):
                raise IOError(errno.ENOENT, os.strerror(errno.ENOENT))
            if path_parts and (path_parts[0].endswith('|') or path_parts[0].endswith(':')):
                path_drive = path_parts.pop(0)
                if path_drive.endswith('|'):
                    path_drive = path_drive[:-1] + ':'
                while path_parts and (not path_parts[0]):
                    path_parts.pop(0)
            else:
                path_drive = ''
            path = path_drive + os.sep + os.path.join(*path_parts)
            if path_drive and (not os.path.splitdrive(path)):
                path = os.sep + os.path.join(path_drive, *path_parts)
            resp.raw = io.open(path, 'rb')
            resp.raw.release_conn = resp.raw.close
    except IOError as e:
        if e.errno == errno.EACCES:
            resp.status_code = codes.forbidden
        elif e.errno == errno.ENOENT:
            resp.status_code = codes.not_found
        else:
            resp.status_code = codes.bad_request
        resp_str = str(e).encode(locale.getpreferredencoding(False))
        resp.raw = BytesIO(resp_str)
        resp.headers['Content-Length'] = len(resp_str)
        resp.raw.release_conn = resp.raw.close
    else:
        resp.status_code = codes.ok
        resp_stat = os.fstat(resp.raw.fileno())
        if stat.S_ISREG(resp_stat.st_mode):
            resp.headers['Content-Length'] = resp_stat.st_size
    return resp