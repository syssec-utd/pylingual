def cli_fordo(context, path=None):
    """
    Issues commands for each item in an account or container listing.

    See :py:mod:`swiftly.cli.fordo` for context usage information.

    See :py:class:`CLIForDo` for more information.
    """
    path = path.lstrip('/') if path else None
    if path and '/' in path:
        raise ReturnCode('path must be an empty string or a container name; was %r' % path)
    limit = context.query.get('limit')
    delimiter = context.query.get('delimiter')
    prefix = context.query.get('prefix')
    marker = context.query.get('marker')
    end_marker = context.query.get('end_marker')
    conc = Concurrency(context.concurrency)
    while True:
        with context.client_manager.with_client() as client:
            if not path:
                status, reason, headers, contents = client.get_account(headers=context.headers, prefix=prefix, delimiter=delimiter, marker=marker, end_marker=end_marker, limit=limit, query=context.query, cdn=context.cdn)
            else:
                status, reason, headers, contents = client.get_container(path, headers=context.headers, prefix=prefix, delimiter=delimiter, marker=marker, end_marker=end_marker, limit=limit, query=context.query, cdn=context.cdn)
            if status // 100 != 2:
                if status == 404 and context.ignore_404:
                    return
                if hasattr(contents, 'read'):
                    contents.read()
                if not path:
                    raise ReturnCode('listing account: %s %s' % (status, reason))
                else:
                    raise ReturnCode('listing container %r: %s %s' % (path, status, reason))
        if not contents:
            break
        for item in contents:
            name = (path + '/' if path else '') + item.get('name', item.get('subdir'))
            args = list(context.remaining_args)
            try:
                index = args.index('<item>')
            except ValueError:
                raise ReturnCode('No "<item>" designation found in the "do" clause.')
            args[index] = name
            for exc_type, exc_value, exc_tb, result in six.itervalues(conc.get_results()):
                if exc_value:
                    conc.join()
                    raise exc_value
            conc.spawn(name, _cli_call, context, name, args)
        marker = contents[-1]['name']
        if limit:
            break
    conc.join()
    for exc_type, exc_value, exc_tb, result in six.itervalues(conc.get_results()):
        if exc_value:
            conc.join()
            raise exc_value