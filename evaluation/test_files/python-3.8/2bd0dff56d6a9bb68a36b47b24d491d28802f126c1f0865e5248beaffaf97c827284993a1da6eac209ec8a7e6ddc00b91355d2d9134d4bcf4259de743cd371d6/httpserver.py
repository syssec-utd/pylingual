import http
import ssl
import sys
from remoshock.httpserver.requesthandler import RequestHandler

class HttpServer:
    """A http server to handle static files and REST comands."""

    def __init__(self, remoshock, args, randomizer):
        self.remoshock = remoshock
        RequestHandler.remoshock = remoshock
        RequestHandler.args = args
        RequestHandler.randomizer = randomizer

    def start_web_server(self):
        """starts the webserver on the tcp-port which is configured in remoshock.ini"""
        port = self.remoshock.config.getint('global', 'web_port', fallback=7777)
        print()
        print('Open http://127.0.0.1:' + str(port) + '/#token=' + self.remoshock.config.get('global', 'web_authentication_token'))
        print()
        server = http.server.ThreadingHTTPServer(('0.0.0.0', port), RequestHandler)
        certfile = self.remoshock.config.get('global', 'web_server_certfile', fallback=None)
        if certfile:
            server.socket = ssl.wrap_socket(server.socket, certfile=certfile, ssl_version=ssl.PROTOCOL_TLSv1_2, server_side=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('Stopped by Ctrl+c.')
            sys.exit(0)