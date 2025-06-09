def _read_namespaced(ctx: ReaderContext, allowed_suffix: Optional[str]=None) -> Tuple[Optional[str], str]:
    """Read a namespaced token from the input stream."""
    ns: List[str] = []
    name: List[str] = []
    reader = ctx.reader
    has_ns = False
    while True:
        token = reader.peek()
        if token == '/':
            reader.next_token()
            if has_ns:
                raise SyntaxError("Found '/'; expected word character")
            elif len(name) == 0:
                name.append('/')
            else:
                if '/' in name:
                    raise SyntaxError("Found '/' after '/'")
                has_ns = True
                ns = name
                name = []
        elif ns_name_chars.match(token):
            reader.next_token()
            name.append(token)
        elif allowed_suffix is not None and token == allowed_suffix:
            reader.next_token()
            name.append(token)
        else:
            break
    ns_str = None if not has_ns else ''.join(ns)
    name_str = ''.join(name)
    if ns_str is None:
        if '/' in name_str and name_str != '/':
            raise SyntaxError("'/' character disallowed in names")
    assert ns_str is None or len(ns_str) > 0
    return (ns_str, name_str)