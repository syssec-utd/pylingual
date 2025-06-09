def _decode_thrift_span(self, thrift_span):
    """Decodes a thrift span.

        :param thrift_span: thrift span
        :type thrift_span: thrift Span object
        :returns: span builder representing this span
        :rtype: Span
        """
    parent_id = None
    local_endpoint = None
    annotations = {}
    tags = {}
    kind = Kind.LOCAL
    remote_endpoint = None
    timestamp = None
    duration = None
    if thrift_span.parent_id:
        parent_id = self._convert_unsigned_long_to_lower_hex(thrift_span.parent_id)
    if thrift_span.annotations:
        annotations, local_endpoint, kind, timestamp, duration = self._decode_thrift_annotations(thrift_span.annotations)
    if thrift_span.binary_annotations:
        tags, local_endpoint, remote_endpoint = self._convert_from_thrift_binary_annotations(thrift_span.binary_annotations)
    trace_id = self._convert_trace_id_to_string(thrift_span.trace_id, thrift_span.trace_id_high)
    return Span(trace_id=trace_id, name=thrift_span.name, parent_id=parent_id, span_id=self._convert_unsigned_long_to_lower_hex(thrift_span.id), kind=kind, timestamp=self.seconds(timestamp or thrift_span.timestamp), duration=self.seconds(duration or thrift_span.duration), local_endpoint=local_endpoint, remote_endpoint=remote_endpoint, shared=kind == Kind.SERVER and thrift_span.timestamp is None, annotations=annotations, tags=tags)