def images(self, query=None):
    """List local images in the database, optionally with a query.

       Paramters
       =========
       query: a string to search for in the container or collection name|tag|uri

    """
    from sregistry.database.models import Collection, Container
    rows = []
    if query is not None:
        like = '%' + query + '%'
        containers = Container.query.filter(or_(Container.name == query, Container.tag.like(like), Container.uri.like(like), Container.name.like(like))).all()
    else:
        containers = Container.query.all()
    if len(containers) > 0:
        message = '  [date]   [client]\t[uri]'
        bot.custom(prefix='Containers:', message=message, color='RED')
        for c in containers:
            uri = c.get_uri()
            created_at = c.created_at.strftime('%B %d, %Y')
            rows.append([created_at, '   [%s]' % c.client, uri])
        bot.table(rows)
    return containers