def process_image(self, image, image_format, save_kwargs={}):
    """Return a BytesIO instance of `image` with inverted colors."""
    imagefile = BytesIO()
    inv_image = ImageOps.invert(image)
    inv_image.save(imagefile, **save_kwargs)
    return imagefile