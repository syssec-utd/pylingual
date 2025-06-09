def _scale_size(size, scale):
    """Rescale a size by a ratio.

    Args:
        size (tuple): w, h.
        scale (float): Scaling factor.

    Returns:
        tuple[int]: scaled size.
    """
    (w, h) = size
    return (int(w * float(scale) + 0.5), int(h * float(scale) + 0.5))