def search(self, query):
    """ Search the database for the given query. Will find partial matches. """
    results = self.session.query(Domain).filter(Domain.name.ilike('%%%s%%' % query)).all()
    return results