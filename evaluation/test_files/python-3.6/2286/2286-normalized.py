def residual_degrees_of_freedom(self, train=False, valid=False, xval=False):
    """
        Retreive the residual degress of freedom if this model has the attribute, or None otherwise.

        :param bool train: Get the residual dof for the training set. If both train and valid are False, then train
            is selected by default.
        :param bool valid: Get the residual dof for the validation set. If both train and valid are True, then train
            is selected by default.

        :returns: Return the residual dof, or None if it is not present.
        """
    if xval:
        raise H2OValueError('Cross-validation metrics are not available.')
    if not train and (not valid):
        train = True
    if train and valid:
        train = True
    if train:
        return self._model_json['output']['training_metrics'].residual_degrees_of_freedom()
    else:
        return self._model_json['output']['validation_metrics'].residual_degrees_of_freedom()