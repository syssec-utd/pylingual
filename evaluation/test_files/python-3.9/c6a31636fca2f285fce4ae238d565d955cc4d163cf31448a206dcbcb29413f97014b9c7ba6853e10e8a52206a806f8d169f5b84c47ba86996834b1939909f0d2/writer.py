class Writer(object):

    def __init__(self):
        pass

    def write_scalar(self, iteration_num, scalar):
        """ Write scalar with your favorite tools

        Args:
            iteration_num (int): iteration number
            scalar (dict): scalar of the latest iteration state
        """
        pass

    def write_histogram(self, iteration_num, histogram):
        """ Write histogram with your favorite tools

        Args:
            iteration_num (int): iteration number
            histogram: histogram of the latest iteration state
        """
        pass

    def write_image(self, iteration_num, image):
        """ Write image with your favorite tools

        Args:
            iteration_num (int): iteration number
            image: image of the latest iteration state
        """
        pass