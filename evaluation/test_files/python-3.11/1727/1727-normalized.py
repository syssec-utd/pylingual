def get_mnist(data_type='train', location='/tmp/mnist'):
    """
    Get mnist dataset with features and label as ndarray.
    Data would be downloaded automatically if it doesn't present at the specific location.

    :param data_type: "train" for training data and "test" for testing data.
    :param location: Location to store mnist dataset.
    :return: (features: ndarray, label: ndarray)
    """
    X, Y = mnist.read_data_sets(location, data_type)
    return (X, Y + 1)