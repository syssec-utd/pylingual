def set_option(self, key, value):
    """Sets general options used by plugins and streams originating
        from this session object.

        :param key: key of the option
        :param value: value to set the option to


        **Available options**:

        ======================== =========================================
        hds-live-edge            ( float) Specify the time live HDS
                                 streams will start from the edge of
                                 stream, default: ``10.0``

        hds-segment-attempts     (int) How many attempts should be done
                                 to download each HDS segment, default: ``3``

        hds-segment-threads      (int) The size of the thread pool used
                                 to download segments, default: ``1``

        hds-segment-timeout      (float) HDS segment connect and read
                                 timeout, default: ``10.0``

        hds-timeout              (float) Timeout for reading data from
                                 HDS streams, default: ``60.0``

        hls-live-edge            (int) How many segments from the end
                                 to start live streams on, default: ``3``

        hls-segment-attempts     (int) How many attempts should be done
                                 to download each HLS segment, default: ``3``

        hls-segment-threads      (int) The size of the thread pool used
                                 to download segments, default: ``1``

        hls-segment-timeout      (float) HLS segment connect and read
                                 timeout, default: ``10.0``

        hls-timeout              (float) Timeout for reading data from
                                 HLS streams, default: ``60.0``

        http-proxy               (str) Specify a HTTP proxy to use for
                                 all HTTP requests

        https-proxy              (str) Specify a HTTPS proxy to use for
                                 all HTTPS requests

        http-cookies             (dict or str) A dict or a semi-colon (;)
                                 delimited str of cookies to add to each
                                 HTTP request, e.g. ``foo=bar;baz=qux``

        http-headers             (dict or str) A dict or semi-colon (;)
                                 delimited str of headers to add to each
                                 HTTP request, e.g. ``foo=bar;baz=qux``

        http-query-params        (dict or str) A dict or a ampersand (&)
                                 delimited string of query parameters to
                                 add to each HTTP request,
                                 e.g. ``foo=bar&baz=qux``

        http-trust-env           (bool) Trust HTTP settings set in the
                                 environment, such as environment
                                 variables (HTTP_PROXY, etc) and
                                 ~/.netrc authentication

        http-ssl-verify          (bool) Verify SSL certificates,
                                 default: ``True``

        http-ssl-cert            (str or tuple) SSL certificate to use,
                                 can be either a .pem file (str) or a
                                 .crt/.key pair (tuple)

        http-timeout             (float) General timeout used by all HTTP
                                 requests except the ones covered by
                                 other options, default: ``20.0``

        http-stream-timeout      (float) Timeout for reading data from
                                 HTTP streams, default: ``60.0``

        subprocess-errorlog      (bool) Log errors from subprocesses to
                                 a file located in the temp directory

        subprocess-errorlog-path (str) Log errors from subprocesses to
                                 a specific file

        ringbuffer-size          (int) The size of the internal ring
                                 buffer used by most stream types,
                                 default: ``16777216`` (16MB)

        rtmp-proxy               (str) Specify a proxy (SOCKS) that RTMP
                                 streams will use

        rtmp-rtmpdump            (str) Specify the location of the
                                 rtmpdump executable used by RTMP streams,
                                 e.g. ``/usr/local/bin/rtmpdump``

        rtmp-timeout             (float) Timeout for reading data from
                                 RTMP streams, default: ``60.0``

        ffmpeg-ffmpeg            (str) Specify the location of the
                                 ffmpeg executable use by Muxing streams
                                 e.g. ``/usr/local/bin/ffmpeg``

        ffmpeg-verbose           (bool) Log stderr from ffmpeg to the
                                 console

        ffmpeg-verbose-path      (str) Specify the location of the
                                 ffmpeg stderr log file

        ffmpeg-video-transcode   (str) The codec to use if transcoding
                                 video when muxing with ffmpeg
                                 e.g. ``h264``

        ffmpeg-audio-transcode   (str) The codec to use if transcoding
                                 audio when muxing with ffmpeg
                                 e.g. ``aac``

        stream-segment-attempts  (int) How many attempts should be done
                                 to download each segment, default: ``3``.
                                 General option used by streams not
                                 covered by other options.

        stream-segment-threads   (int) The size of the thread pool used
                                 to download segments, default: ``1``.
                                 General option used by streams not
                                 covered by other options.

        stream-segment-timeout   (float) Segment connect and read
                                 timeout, default: ``10.0``.
                                 General option used by streams not
                                 covered by other options.

        stream-timeout           (float) Timeout for reading data from
                                 stream, default: ``60.0``.
                                 General option used by streams not
                                 covered by other options.

        locale                   (str) Locale setting, in the RFC 1766 format
                                 eg. en_US or es_ES
                                 default: ``system locale``.

        user-input-requester     (UserInputRequester) instance of UserInputRequester
                                 to collect input from the user at runtime. Must be
                                 set before the plugins are loaded.
                                 default: ``UserInputRequester``.
        ======================== =========================================

        """
    if key == 'rtmpdump':
        key = 'rtmp-rtmpdump'
    elif key == 'rtmpdump-proxy':
        key = 'rtmp-proxy'
    elif key == 'errorlog':
        key = 'subprocess-errorlog'
    elif key == 'errorlog-path':
        key = 'subprocess-errorlog-path'
    if key == 'http-proxy':
        self.http.proxies['http'] = update_scheme('http://', value)
    elif key == 'https-proxy':
        self.http.proxies['https'] = update_scheme('https://', value)
    elif key == 'http-cookies':
        if isinstance(value, dict):
            self.http.cookies.update(value)
        else:
            self.http.parse_cookies(value)
    elif key == 'http-headers':
        if isinstance(value, dict):
            self.http.headers.update(value)
        else:
            self.http.parse_headers(value)
    elif key == 'http-query-params':
        if isinstance(value, dict):
            self.http.params.update(value)
        else:
            self.http.parse_query_params(value)
    elif key == 'http-trust-env':
        self.http.trust_env = value
    elif key == 'http-ssl-verify':
        self.http.verify = value
    elif key == 'http-disable-dh':
        if value:
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':!DH'
            try:
                requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST = requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS.encode('ascii')
            except AttributeError:
                pass
    elif key == 'http-ssl-cert':
        self.http.cert = value
    elif key == 'http-timeout':
        self.http.timeout = value
    else:
        self.options.set(key, value)