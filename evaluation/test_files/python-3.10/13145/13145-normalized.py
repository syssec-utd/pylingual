def get_metric(self, name: str, labels: Union[Dict[str, str], None]=None) -> Metric:
    """Return a metric, optionally configured with labels."""
    metric = self._metrics[name]
    if labels:
        return metric.labels(**labels)
    return metric