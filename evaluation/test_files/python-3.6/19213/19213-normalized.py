def srid(self):
    """Returns the EPSG ID as int if it exists."""
    epsg_id = self.GetAuthorityCode('PROJCS') or self.GetAuthorityCode('GEOGCS')
    try:
        return int(epsg_id)
    except TypeError:
        return