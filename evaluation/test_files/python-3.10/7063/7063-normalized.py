def process_bind_param(self, value, dialect):
    """
        Returns the integer value of the usage mask bitmask. This value is
        stored in the database.

        Args:
            value(list<enums.CryptographicUsageMask>): list of enums in the
            usage mask
            dialect(string): SQL dialect
        """
    bitmask = 0
    for e in value:
        bitmask = bitmask | e.value
    return bitmask