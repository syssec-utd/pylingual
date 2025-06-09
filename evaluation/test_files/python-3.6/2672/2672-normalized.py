def get_metrics_data_queue(self, name, queue_name, metric, rollup, filter_expresssion):
    """
        Retrieves the list of supported metrics for this namespace and queue

        name:
            Name of the service bus namespace.
        queue_name:
            Name of the service bus queue in this namespace.
        metric:
            name of a supported metric
        rollup:
            name of a supported rollup
        filter_expression:
            filter, for instance "$filter=Timestamp gt datetime'2014-10-01T00:00:00Z'"
        """
    response = self._perform_get(self._get_get_metrics_data_queue_path(name, queue_name, metric, rollup, filter_expresssion), None)
    return _MinidomXmlToObject.convert_response_to_feeds(response, partial(_ServiceBusManagementXmlSerializer.xml_to_metrics, object_type=MetricValues))