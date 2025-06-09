def track_metric(self, name: str, value: float, type: TelemetryDataPointType=None, count: int=None, min: float=None, max: float=None, std_dev: float=None, properties: Dict[str, object]=None) -> NotImplemented:
    """
        Send information about a single metric data point that was captured for the application.
        :param name: The name of the metric that was captured.
        :param value: The value of the metric that was captured.
        :param type: The type of the metric. (defaults to: TelemetryDataPointType.aggregation`)
        :param count: the number of metrics that were aggregated into this data point. (defaults to: None)
        :param min: the minimum of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param max: the maximum of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param std_dev: the standard deviation of all metrics collected that were aggregated into this data point. (defaults to: None)
        :param properties: the set of custom properties the client wants attached to this data item. (defaults to: None)
        """
    self._client.track_metric(name, value, type, count, min, max, std_dev, properties)