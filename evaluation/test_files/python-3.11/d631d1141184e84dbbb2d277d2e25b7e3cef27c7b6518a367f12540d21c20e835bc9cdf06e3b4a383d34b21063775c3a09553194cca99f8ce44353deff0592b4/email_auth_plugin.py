import logging
import smtplib

class EmailAuthPlugin:
    name = 'email_auth'
    label = 'Email'

    def __init__(self, server='smtp.gmail.com:587', domain='@gmail.com', tls_mode=None):
        self.server = server
        self.domain = domain
        self.tls_mode = tls_mode

    def validate_credentials(self, username, password):
        email = username
        server = self.server
        domain = self.domain
        tls_mode = self.tls_mode
        if domain:
            if not isinstance(domain, (list, tuple)):
                domain = [str(domain)]
            if not [d for d in domain if email[-len(d):] == d]:
                return False
        if ':' in server:
            host, port = server.split(':')
        else:
            host = server
            port = 25
        if tls_mode is None:
            tls_mode = port == '587'
        try:
            server = None
            server = smtplib.SMTP(host, port)
            server.ehlo()
            if tls_mode:
                server.starttls()
                server.ehlo()
            server.login(email, password)
            server.quit()
            return True
        except:
            logging.exception('email_auth() failed')
            if server:
                try:
                    server.quit()
                except:
                    pass
            return False