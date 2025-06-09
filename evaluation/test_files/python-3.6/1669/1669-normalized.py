def random_split(self, weights):
    """
        Random split imageframes according to weights
        :param weights: weights for each ImageFrame
        :return: 
        """
    jvalues = self.image_frame.random_split(weights)
    return [ImageFrame(jvalue) for jvalue in jvalues]