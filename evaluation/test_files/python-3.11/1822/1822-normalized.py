def roc_auc_score(y_true: Union[List[List[float]], List[List[int]], np.ndarray], y_pred: Union[List[List[float]], List[List[int]], np.ndarray]) -> float:
    """
    Compute Area Under the Curve (AUC) from prediction scores.

    Args:
        y_true: true binary labels
        y_pred: target scores, can either be probability estimates of the positive class

    Returns:
        Area Under the Curve (AUC) from prediction scores
    """
    try:
        return sklearn.metrics.roc_auc_score(np.squeeze(np.array(y_true)), np.squeeze(np.array(y_pred)), average='macro')
    except ValueError:
        return 0.0