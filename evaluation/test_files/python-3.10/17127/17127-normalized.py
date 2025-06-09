def get_backdoor_server(self, listen_addr, **context):
    """Add a backdoor (debug) server."""
    from django.conf import settings
    local_vars = {'launcher': self, 'servers': self.servers, 'pgworker': self.pgworker, 'stop': self.stop, 'api': self.api, 'resource': self.resource, 'settings': settings, 'wsgi_app': self.wsgi_app, 'wsgi_name': self.wsgi_name}
    local_vars.update(context)
    return BackdoorServer(listen_addr, banner='Django DDP', locals=local_vars)