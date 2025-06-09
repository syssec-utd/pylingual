def _get_protobuf_kind(kind):
    """Converts py_zipkin's Kind to Protobuf's Kind.

    :param kind: py_zipkin's Kind.
    :type kind: py_zipkin.Kind
    :return: correcponding protobuf's kind value.
    :rtype: zipkin_pb2.Span.Kind
    """
    if kind == Kind.CLIENT:
        return zipkin_pb2.Span.CLIENT
    elif kind == Kind.SERVER:
        return zipkin_pb2.Span.SERVER
    elif kind == Kind.PRODUCER:
        return zipkin_pb2.Span.PRODUCER
    elif kind == Kind.CONSUMER:
        return zipkin_pb2.Span.CONSUMER
    return None