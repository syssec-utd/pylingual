def crop_image(img, start_y, start_x, h, w):
    """
    Crop an image given the top left corner.
    :param img: The image
    :param start_y: The top left corner y coord
    :param start_x: The top left corner x coord
    :param h: The result height
    :param w: The result width
    :return: The cropped image.
    """
    return img[start_y:start_y + h, start_x:start_x + w, :].copy()