def create_resized_image(self, path_to_image, save_path_on_storage, width, height):
    """
        Create a resized image.

        `path_to_image`: The path to the image with the media directory to
                         resize. If `None`, the
                         VERSATILEIMAGEFIELD_PLACEHOLDER_IMAGE will be used.
        `save_path_on_storage`: Where on self.storage to save the resized image
        `width`: Width of resized image (int)
        `height`: Desired height of resized image (int)
        `filename_key`: A string that will be used in the sized image filename
                        to signify what operation was done to it.
                        Examples: 'crop' or 'scale'
        """
    image, file_ext, image_format, mime_type = self.retrieve_image(path_to_image)
    image, save_kwargs = self.preprocess(image, image_format)
    imagefile = self.process_image(image=image, image_format=image_format, save_kwargs=save_kwargs, width=width, height=height)
    self.save_image(imagefile, save_path_on_storage, file_ext, mime_type)