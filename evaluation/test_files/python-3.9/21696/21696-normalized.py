def new_author(name=None, email=None, affiliation=None, url=None):
    """Create a new author."""
    author = NotebookNode()
    if name is not None:
        author.name = unicode(name)
    if email is not None:
        author.email = unicode(email)
    if affiliation is not None:
        author.affiliation = unicode(affiliation)
    if url is not None:
        author.url = unicode(url)
    return author