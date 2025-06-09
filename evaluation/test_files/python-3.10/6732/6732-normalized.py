def get_mask(self, layers=None, output='vector', in_global_mask=True):
    """ Set the current mask by taking the conjunction of all specified
        layers.

        Args:
            layers: Which layers to include. See documentation for add() for
                format.
            include_global_mask: Whether or not to automatically include the
                global mask (i.e., self.volume) in the conjunction.
        """
    if in_global_mask:
        output = 'vector'
    if layers is None:
        layers = self.layers.keys()
    elif not isinstance(layers, list):
        layers = [layers]
    layers = map(lambda x: x if isinstance(x, string_types) else self.stack[x], layers)
    layers = [self.layers[l] for l in layers if l in self.layers]
    layers.append(self.full)
    layers = np.vstack(layers).T.astype(bool)
    mask = layers.all(axis=1)
    mask = self.get_image(mask, output)
    return mask[self.global_mask] if in_global_mask else mask