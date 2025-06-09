def warp(self, to_sref, dest=None, interpolation=gdalconst.GRA_NearestNeighbour):
    """Returns a new reprojected instance.

        Arguments:
        to_sref -- spatial reference as a proj4 or wkt string, or a
        SpatialReference
        Keyword args:
        dest -- filepath as str
        interpolation -- GDAL interpolation type
        """
    if not hasattr(to_sref, 'ExportToWkt'):
        to_sref = SpatialReference(to_sref)
    dest_wkt = to_sref.ExportToWkt()
    dtype = self[0].DataType
    err_thresh = 0.125
    vrt = gdal.AutoCreateWarpedVRT(self.ds, None, dest_wkt, interpolation, err_thresh)
    if vrt is None:
        raise ValueError('Could not warp %s to %s' % (self, dest_wkt))
    warpsize = (vrt.RasterXSize, vrt.RasterYSize, len(self))
    warptrans = vrt.GetGeoTransform()
    vrt = None
    if dest is None:
        imgio = MemFileIO()
        rwarp = self.driver.raster(imgio, warpsize, dtype)
        imgio.close()
    else:
        rwarp = self.driver.raster(dest, warpsize, dtype)
    rwarp.SetGeoTransform(warptrans)
    rwarp.SetProjection(to_sref)
    if self.nodata is not None:
        for band in rwarp:
            band.SetNoDataValue(self.nodata)
            band = None
    gdal.ReprojectImage(self.ds, rwarp.ds, None, None, interpolation)
    return rwarp