def transformCartesianCoordinates(self, x, y, z):
    """
        Rotates Cartesian coordinates from one reference system to another using the rotation matrix with
        which the class was initialized. The inputs  can be scalars or 1-dimensional numpy arrays.

        Parameters
        ----------

        x - Value of X-coordinate in original reference system
        y - Value of Y-coordinate in original reference system
        z - Value of Z-coordinate in original reference system

        Returns
        -------

        xrot - Value of X-coordinate after rotation
        yrot - Value of Y-coordinate after rotation
        zrot - Value of Z-coordinate after rotation
        """
    xrot, yrot, zrot = dot(self.rotationMatrix, [x, y, z])
    return (xrot, yrot, zrot)