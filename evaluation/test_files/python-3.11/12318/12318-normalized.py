def request(self, method, path, contents, headers, decode_json=False, stream=False, query=None, cdn=False):
    """
        See :py:func:`swiftly.client.client.Client.request`
        """
    if query:
        path += '?' + '&'.join(('%s=%s' % (quote(k), quote(v)) if v else quote(k) for k, v in sorted(six.iteritems(query))))
    reset_func = self._default_reset_func
    if isinstance(contents, six.string_types):
        contents = StringIO(contents)
    tell = getattr(contents, 'tell', None)
    seek = getattr(contents, 'seek', None)
    if tell and seek:
        try:
            orig_pos = tell()
            reset_func = lambda: seek(orig_pos)
        except Exception:
            tell = seek = None
    elif not contents:
        reset_func = lambda: None
    status = 0
    reason = 'Unknown'
    attempt = 0
    while attempt < self.attempts:
        attempt += 1
        if time() >= self.conn_discard:
            self.storage_conn = None
            self.cdn_conn = None
        if cdn:
            conn = self.cdn_conn
            conn_path = self.cdn_path
        else:
            conn = self.storage_conn
            conn_path = self.storage_path
        if not conn:
            parsed, conn = self._connect(cdn=cdn)
            if conn:
                if cdn:
                    self.cdn_conn = conn
                    self.cdn_path = conn_path = parsed.path
                else:
                    self.storage_conn = conn
                    self.storage_path = conn_path = parsed.path
            else:
                raise self.HTTPException('%s %s failed: No connection' % (method, path))
        self.conn_discard = time() + 4
        titled_headers = dict(((k.title(), v) for k, v in six.iteritems({'User-Agent': self.user_agent, 'X-Auth-Token': self.auth_token})))
        if headers:
            titled_headers.update(((k.title(), v) for k, v in six.iteritems(headers)))
        try:
            if not hasattr(contents, 'read'):
                if method not in self.no_content_methods and contents and ('Content-Length' not in titled_headers) and ('Transfer-Encoding' not in titled_headers):
                    titled_headers['Content-Length'] = str(len(contents or ''))
                verbose_headers = '  '.join(('%s: %s' % (k, v) for k, v in sorted(six.iteritems(titled_headers))))
                self.verbose('> %s %s %s', method, conn_path + path, verbose_headers)
                conn.request(method, conn_path + path, contents, titled_headers)
            else:
                conn.putrequest(method, conn_path + path)
                content_length = None
                for h, v in sorted(six.iteritems(titled_headers)):
                    if h == 'Content-Length':
                        content_length = int(v)
                    conn.putheader(h, v)
                if method not in self.no_content_methods and content_length is None:
                    titled_headers['Transfer-Encoding'] = 'chunked'
                    conn.putheader('Transfer-Encoding', 'chunked')
                conn.endheaders()
                verbose_headers = '  '.join(('%s: %s' % (k, v) for k, v in sorted(six.iteritems(titled_headers))))
                self.verbose('> %s %s %s', method, conn_path + path, verbose_headers)
                if method not in self.no_content_methods and content_length is None:
                    chunk = contents.read(self.chunk_size)
                    while chunk:
                        conn.send('%x\r\n%s\r\n' % (len(chunk), chunk))
                        chunk = contents.read(self.chunk_size)
                    conn.send('0\r\n\r\n')
                else:
                    left = content_length or 0
                    while left > 0:
                        size = self.chunk_size
                        if size > left:
                            size = left
                        chunk = contents.read(size)
                        if not chunk:
                            raise IOError('Early EOF from input')
                        conn.send(chunk)
                        left -= len(chunk)
            resp = conn.getresponse()
            status = resp.status
            reason = resp.reason
            hdrs = headers_to_dict(resp.getheaders())
            if stream:
                value = resp
            else:
                value = resp.read()
                resp.close()
        except Exception as err:
            status = 0
            reason = '%s %s' % (type(err), str(err))
            hdrs = {}
            value = None
        self.verbose('< %s %s', status or '-', reason)
        self.verbose('< %s', hdrs)
        if status == 401:
            if stream:
                value.close()
            conn.close()
            self.auth()
            attempt -= 1
        elif status and status // 100 != 5:
            if not stream and decode_json and (status // 100 == 2):
                if value:
                    value = json.loads(value.decode('utf-8'))
                else:
                    value = None
            self.conn_discard = time() + 4
            return (status, reason, hdrs, value)
        else:
            if stream and value:
                value.close()
            conn.close()
        if reset_func:
            reset_func()
        self.sleep(2 ** attempt)
    raise self.HTTPException('%s %s failed: %s %s' % (method, path, status, reason))