def parse(cls, parser, token):
    """
        Parse the "as var" syntax.
        """
    bits, as_var = parse_as_var(parser, token)
    tag_name, args, kwargs = parse_token_kwargs(parser, bits, ('template',) + cls.allowed_kwargs, compile_args=cls.compile_args, compile_kwargs=cls.compile_kwargs)
    cls.validate_args(tag_name, *args)
    return cls(tag_name, as_var, *args, **kwargs)