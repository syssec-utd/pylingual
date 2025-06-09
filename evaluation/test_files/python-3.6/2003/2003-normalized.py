def h2o_mean_squared_error(y_actual, y_predicted, weights=None):
    """
    Mean squared error regression loss

    :param y_actual: H2OFrame of actual response.
    :param y_predicted: H2OFrame of predicted response.
    :param weights: (Optional) sample weights
    :returns: mean squared error loss (best is 0.0).
    """
    ModelBase._check_targets(y_actual, y_predicted)
    return _colmean((y_predicted - y_actual) ** 2)