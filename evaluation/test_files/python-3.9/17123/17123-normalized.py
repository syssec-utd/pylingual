def main():
    """Main entry point for `dddp` command."""
    parser = argparse.ArgumentParser(description=__doc__)
    django = parser.add_argument_group('Django Options')
    django.add_argument('--verbosity', '-v', metavar='VERBOSITY', dest='verbosity', type=int, default=1)
    django.add_argument('--debug-port', metavar='DEBUG_PORT', dest='debug_port', type=int, default=0)
    django.add_argument('--settings', metavar='SETTINGS', dest='settings', help='The Python path to a settings module, e.g. "myproject.settings.main". If this isn\'t provided, the DJANGO_SETTINGS_MODULE environment variable will be used.')
    http = parser.add_argument_group('HTTP Options')
    http.add_argument('listen', metavar='address[:port]', nargs='*', type=addr, help='Listening address for HTTP(s) server.')
    ssl = parser.add_argument_group('SSL Options')
    ssl.add_argument('--ssl-version', metavar='SSL_VERSION', dest='ssl_version', help="SSL version to use (see stdlib ssl module's) [3]", choices=['1', '2', '3'], default='3')
    ssl.add_argument('--certfile', metavar='FILE', dest='certfile', help='SSL certificate file [None]')
    ssl.add_argument('--ciphers', metavar='CIPHERS', dest='ciphers', help="Ciphers to use (see stdlib ssl module's) [TLSv1]")
    ssl.add_argument('--ca-certs', metavar='FILE', dest='ca_certs', help='CA certificates file [None]')
    ssl.add_argument('--keyfile', metavar='FILE', dest='keyfile', help='SSL key file [None]')
    namespace = parser.parse_args()
    if namespace.settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = namespace.settings
    serve(namespace.listen or [Addr('localhost', 8000)], debug_port=namespace.debug_port, keyfile=namespace.keyfile, certfile=namespace.certfile, verbosity=namespace.verbosity)