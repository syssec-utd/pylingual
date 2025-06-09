def dumps(post, handler=None, **kwargs):
    """
    Serialize a :py:class:`post <frontmatter.Post>` to a string and return text. 
    This always returns unicode text, which can then be encoded.

    Passing ``handler`` will change how metadata is turned into text. A handler
    passed as an argument will override ``post.handler``, with 
    :py:class:`YAMLHandler <frontmatter.default_handlers.YAMLHandler>` used as 
    a default.
    ::

        >>> print(frontmatter.dumps(post))
        ---
        excerpt: tl;dr
        layout: post
        title: Hello, world!
        ---
        Well, hello there, world.

    """
    if handler is None:
        handler = getattr(post, 'handler', None) or YAMLHandler()
    start_delimiter = kwargs.pop('start_delimiter', handler.START_DELIMITER)
    end_delimiter = kwargs.pop('end_delimiter', handler.END_DELIMITER)
    metadata = handler.export(post.metadata, **kwargs)
    return POST_TEMPLATE.format(metadata=metadata, content=post.content, start_delimiter=start_delimiter, end_delimiter=end_delimiter).strip()