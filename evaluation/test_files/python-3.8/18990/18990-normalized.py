def make_app():
    """Make a WSGI app that has all the HTTPie pieces baked in."""
    env = Environment()
    args = parser.parse_args(args=['/', '--ignore-stdin'], env=env)
    args.output_options = 'HB'
    server = 'HTTPony/{0}'.format(__version__)

    def application(environ, start_response):
        if environ.get('CONTENT_LENGTH') == '':
            del environ['CONTENT_LENGTH']
        if environ.get('CONTENT_TYPE') == '':
            del environ['CONTENT_TYPE']
        wrequest = WerkzeugRequest(environ)
        data = wrequest.get_data()
        request = Request(method=wrequest.method, url=wrequest.url, headers=wrequest.headers, data=data)
        prepared = request.prepare()
        stream = streams.build_output_stream(args, env, prepared, response=None, output_options=args.output_options)
        streams.write_stream(stream, env.stdout, env.stdout_isatty)
        if data:
            print('\n', file=env.stdout)
        response = Response(headers={'Server': server})
        return response(environ, start_response)
    return application