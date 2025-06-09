def start(self, context):
    """Construct the SQLAlchemy engine and session factory."""
    if __debug__:
        log.info('Connecting SQLAlchemy database layer.', extra=dict(uri=redact_uri(self.uri), config=self.config, alias=self.alias))
    engine = self.engine = create_engine(self.uri, **self.config)
    self.Session = scoped_session(sessionmaker(bind=engine))
    engine.connect().close()
    context.db[self.alias] = engine