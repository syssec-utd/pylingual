def stop(self, _exc_type=None, _exc_value=None, _exc_traceback=None):
    """Exit the span context. Zipkin attrs are pushed onto the
        threadlocal stack regardless of sampling, so they always need to be
        popped off. The actual logging of spans depends on sampling and that
        the logging was correctly set up.
        """
    if self.do_pop_attrs:
        self.get_tracer().pop_zipkin_attrs()
    if not self.get_tracer().is_transport_configured():
        return
    if any((_exc_type, _exc_value, _exc_traceback)):
        error_msg = u'{0}: {1}'.format(_exc_type.__name__, _exc_value)
        self.update_binary_annotations({ERROR_KEY: error_msg})
    if self.logging_context:
        try:
            self.logging_context.stop()
        except Exception as ex:
            err_msg = 'Error emitting zipkin trace. {}'.format(repr(ex))
            log.error(err_msg)
        finally:
            self.logging_context = None
            self.get_tracer().clear()
            self.get_tracer().set_transport_configured(configured=False)
            return
    end_timestamp = time.time()
    if self.duration:
        duration = self.duration
    else:
        duration = end_timestamp - self.start_timestamp
    endpoint = create_endpoint(self.port, self.service_name, self.host)
    self.get_tracer().add_span(Span(trace_id=self.zipkin_attrs.trace_id, name=self.span_name, parent_id=self.zipkin_attrs.parent_span_id, span_id=self.zipkin_attrs.span_id, kind=self.kind, timestamp=self.timestamp if self.timestamp else self.start_timestamp, duration=duration, annotations=self.annotations, local_endpoint=endpoint, remote_endpoint=self.remote_endpoint, tags=self.binary_annotations))