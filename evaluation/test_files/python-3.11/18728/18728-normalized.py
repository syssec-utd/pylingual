def getTexCoords(self, data):
    """
        Returns the texture coordinates, if any, to accompany the vertices of this region already transformed.
        
        Note that it is recommended to check the :py:attr:`enable_tex` flag first.
        
        Internally uses :py:meth:`Material.transformTexCoords()`\\ .
        """
    return self.material.transformTexCoords(data, self.tex_coords, self.tex_dims)