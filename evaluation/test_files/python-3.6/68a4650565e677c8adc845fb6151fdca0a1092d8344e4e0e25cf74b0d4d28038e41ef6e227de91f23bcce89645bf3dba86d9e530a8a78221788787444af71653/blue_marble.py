"""
A tile source that serves BlueMarble tiles from the internet.
"""
import math
import GridCal.Gui.pySlipQt.tiles_net as tiles_net
TilesetName = 'BlueMarble Tiles'
TilesetShortName = 'BM Tiles'
TilesetVersion = '1.0'
TileServers = ['http://s3.amazonaws.com']
TileURLPath = '/com.modestmaps.bluemarble/{Z}-r{Y}-c{X}.jpg'
TileLevels = range(10)
MaxServerRequests = 2
MaxLRU = 10000
TileWidth = 256
TileHeight = 256
TilesDir = 'blue_marble_tiles'

class BlueMarbleTiles(tiles_net.Tiles):
    """
    An object to source internet tiles for pySlip.
    """

    def __init__(self, tiles_dir=TilesDir, http_proxy=None):
        """Override the base class for these tiles.

        Basically, just fill in the BaseTiles class with values from above
        and provide the Geo2Tile() and Tile2Geo() methods.
        """
        super().__init__(levels=TileLevels, tile_width=TileWidth, tile_height=TileHeight, tiles_dir=tiles_dir, max_lru=MaxLRU, servers=TileServers, url_path=TileURLPath, max_server_requests=MaxServerRequests, http_proxy=http_proxy)

    def Geo2Tile(self, xgeo, ygeo):
        """Convert geo to tile fractional coordinates for level in use.

        geo  tuple of geo coordinates (xgeo, ygeo)

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """
        lat_rad = math.radians(ygeo)
        n = 2.0 ** self.level
        xtile = (xgeo + 180.0) / 360.0 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return (xtile, ytile)

    def Tile2Geo(self, xtile, ytile):
        """Convert tile fractional coordinates to geo for level in use.

        tile  a tupl;e (xtile,ytile) of tile fractional coordinates

        Note that we assume the point *is* on the map!

        Code taken from [http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames]
        """
        n = 2.0 ** self.level
        xgeo = xtile / n * 360.0 - 180.0
        yrad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        ygeo = math.degrees(yrad)
        return (xgeo, ygeo)