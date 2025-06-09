def getTex(self, name, category):
    """
        Gets the texture associated with the given name and category.
        
        ``category`` must have been created using :py:meth:`addCategory()` before.
        
        If it was loaded previously, a cached version will be returned.
        If it was not loaded, it will be loaded and inserted into the cache.
        
        See :py:meth:`loadTex()` for more information.
        """
    if category not in self.categoriesTexCache:
        return self.getMissingTex(category)
    if name not in self.categoriesTexCache[category]:
        self.loadTex(name, category)
    return self.categoriesTexCache[category][name]