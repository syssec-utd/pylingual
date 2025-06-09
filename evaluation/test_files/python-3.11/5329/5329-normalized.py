def source_expand(self, source):
    """Expand the wildcards for an S3 path. This emulates the shall expansion
       for wildcards if the input is local path.
    """
    result = []
    if not isinstance(source, list):
        source = [source]
    for src in source:
        tmp = self.opt.recursive
        self.opt.recursive = False
        result += [f['name'] for f in self.s3walk(src, True)]
        self.opt.recursive = tmp
    if len(result) == 0 and (not self.opt.ignore_empty_source):
        fail("[Runtime Failure] Source doesn't exist.")
    return result