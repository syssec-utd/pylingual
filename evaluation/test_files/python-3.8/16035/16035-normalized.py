def locate_unbalanced_start(unbalanced_start, pre_delete, post_delete):
    """ pre_delete and post_delete implicitly point to a place in the
    document (where the two were split).  This moves that point (by
    popping items from one and pushing them onto the other).  It moves
    the point to try to find a place where unbalanced_start applies.

    As an example::

        >>> unbalanced_start = ['<div>']
        >>> doc = ['<p>', 'Text', '</p>', '<div>', 'More Text', '</div>']
        >>> pre, post = doc[:3], doc[3:]
        >>> pre, post
        (['<p>', 'Text', '</p>'], ['<div>', 'More Text', '</div>'])
        >>> locate_unbalanced_start(unbalanced_start, pre, post)
        >>> pre, post
        (['<p>', 'Text', '</p>', '<div>'], ['More Text', '</div>'])

    As you can see, we moved the point so that the dangling <div> that
    we found will be effectively replaced by the div in the original
    document.  If this doesn't work out, we just throw away
    unbalanced_start without doing anything.
    """
    while 1:
        if not unbalanced_start:
            break
        finding = unbalanced_start[0]
        finding_name = finding.split()[0].strip('<>')
        if not post_delete:
            break
        next = post_delete[0]
        if next is DEL_START or not next.startswith('<'):
            break
        if next[1] == '/':
            break
        name = next.split()[0].strip('<>')
        if name == 'ins':
            break
        assert name != 'del', 'Unexpected delete tag: %r' % next
        if name == finding_name:
            unbalanced_start.pop(0)
            pre_delete.append(post_delete.pop(0))
        else:
            break