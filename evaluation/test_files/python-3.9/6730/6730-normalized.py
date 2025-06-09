def mask(self, image, nan_to_num=True, layers=None, in_global_mask=False):
    """ Vectorize an image and mask out all invalid voxels.

        Args:
            images: The image to vectorize and mask. Input can be any object
                handled by get_image().
            layers: Which mask layers to use (specified as int, string, or
                list of ints and strings). When None, applies the conjunction
                of all layers.
            nan_to_num: boolean indicating whether to convert NaNs to 0.
            in_global_mask: Whether to return the resulting masked vector in
                the globally masked space (i.e., n_voxels =
                len(self.global_mask)). If False (default), returns in the full
                image space (i.e., n_voxels = len(self.volume)).
        Returns:
          A 1D NumPy array of in-mask voxels.
        """
    self.set_mask(layers)
    image = self.get_image(image, output='vector')
    if in_global_mask:
        masked_data = image[self.global_mask]
        masked_data[~self.get_mask(in_global_mask=True)] = 0
    else:
        masked_data = image[self.current_mask]
    if nan_to_num:
        masked_data = np.nan_to_num(masked_data)
    return masked_data