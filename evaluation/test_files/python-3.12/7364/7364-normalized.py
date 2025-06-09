def create_attrs_for_span(sample_rate=100.0, trace_id=None, span_id=None, use_128bit_trace_id=False):
    """Creates a set of zipkin attributes for a span.

    :param sample_rate: Float between 0.0 and 100.0 to determine sampling rate
    :type sample_rate: float
    :param trace_id: Optional 16-character hex string representing a trace_id.
                    If this is None, a random trace_id will be generated.
    :type trace_id: str
    :param span_id: Optional 16-character hex string representing a span_id.
                    If this is None, a random span_id will be generated.
    :type span_id: str
    :param use_128bit_trace_id: If true, generate 128-bit trace_ids
    :type use_128bit_trace_id: boolean
    """
    if trace_id is None:
        if use_128bit_trace_id:
            trace_id = generate_random_128bit_string()
        else:
            trace_id = generate_random_64bit_string()
    if span_id is None:
        span_id = generate_random_64bit_string()
    if sample_rate == 0.0:
        is_sampled = False
    else:
        is_sampled = random.random() * 100 < sample_rate
    return ZipkinAttrs(trace_id=trace_id, span_id=span_id, parent_span_id=None, flags='0', is_sampled=is_sampled)