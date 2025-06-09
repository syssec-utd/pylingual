def get_metrics_data_notification_hub(self, name, hub_name, metric, rollup, filter_expresssion):
    """
        Retrieves the list of supported metrics for this namespace and topic

        name:
            Name of the service bus namespace.
        hub_name:
            Name of the service bus notification hub in this namespace.
        metric:
            name of a supported metric
        rollup:
            name of a supported rollup
        filter_expression:
            filter, for instance "$filter=Timestamp gt datetime'2014-10-01T00:00:00Z'"
        """
    response = self._perform_get(self._get_get_metrics_data_hub_path(name, hub_name, metric, rollup, filter_expresssion), None)
    return _MinidomXmlToObject.convert_response_to_feeds(response, partial(_ServiceBusManagementXmlSerializer.xml_to_metrics, object_type=MetricValues))