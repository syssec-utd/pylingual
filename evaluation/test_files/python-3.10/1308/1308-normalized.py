def _get_static_predicate(pred):
    """Helper function for statically evaluating predicates in `cond`."""
    if pred in {0, 1}:
        pred_value = bool(pred)
    elif isinstance(pred, bool):
        pred_value = pred
    elif isinstance(pred, tf.Tensor):
        pred_value = tf.get_static_value(pred)
        if pred_value is None:
            pred_value = c_api.TF_TryEvaluateConstant_wrapper(pred.graph._c_graph, pred._as_tf_output())
    else:
        raise TypeError('`pred` must be a Tensor, or a Python bool, or 1 or 0. Found instead: {}'.format(pred))
    return pred_value