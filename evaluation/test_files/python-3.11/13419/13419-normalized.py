def __complete_alias(self, prefix: str, name_in_ns: Optional[str]=None) -> Iterable[str]:
    """Return an iterable of possible completions matching the given
        prefix from the list of aliased namespaces. If name_in_ns is given,
        further attempt to refine the list to matching names in that namespace."""
    candidates = filter(Namespace.__completion_matcher(prefix), [(s, n) for s, n in self.aliases])
    if name_in_ns is not None:
        for _, candidate_ns in candidates:
            for match in candidate_ns.__complete_interns(name_in_ns, include_private_vars=False):
                yield f'{prefix}/{match}'
    else:
        for alias, _ in candidates:
            yield f'{alias}/'