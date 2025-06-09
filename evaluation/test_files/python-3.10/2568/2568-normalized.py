def list_subscription_operations(self, start_time=None, end_time=None, object_id_filter=None, operation_result_filter=None, continuation_token=None):
    """
        List subscription operations.

        start_time: Required. An ISO8601 date.
        end_time: Required. An ISO8601 date.
        object_id_filter: Optional. Returns subscription operations only for the specified object type and object ID
        operation_result_filter: Optional. Returns subscription operations only for the specified result status, either Succeeded, Failed, or InProgress.
        continuation_token: Optional.
        More information at:
        https://msdn.microsoft.com/en-us/library/azure/gg715318.aspx
        """
    start_time = 'StartTime=' + start_time if start_time else ''
    end_time = 'EndTime=' + end_time if end_time else ''
    object_id_filter = 'ObjectIdFilter=' + object_id_filter if object_id_filter else ''
    operation_result_filter = 'OperationResultFilter=' + operation_result_filter if operation_result_filter else ''
    continuation_token = 'ContinuationToken=' + continuation_token if continuation_token else ''
    parameters = '&'.join((v for v in (start_time, end_time, object_id_filter, operation_result_filter, continuation_token) if v))
    parameters = '?' + parameters if parameters else ''
    return self._perform_get(self._get_list_subscription_operations_path() + parameters, SubscriptionOperationCollection)