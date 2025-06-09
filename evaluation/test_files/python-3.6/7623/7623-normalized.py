def SecurityLevel():
    """
    Generates a filter chain for validating a security level.
    """
    return f.Type(int) | f.Min(1) | f.Max(3) | f.Optional(default=AddressGenerator.DEFAULT_SECURITY_LEVEL)