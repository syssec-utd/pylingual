def ready(self):
    """Initialisation for django-ddp (setup lookups and signal handlers)."""
    if not settings.DATABASES:
        raise ImproperlyConfigured('No databases configured.')
    for alias, conf in settings.DATABASES.items():
        engine = conf['ENGINE']
        if engine not in ['django.db.backends.postgresql', 'django.db.backends.postgresql_psycopg2']:
            warnings.warn('Database %r uses unsupported %r engine.' % (alias, engine), UserWarning)
    self.api = autodiscover()
    self.api.ready()