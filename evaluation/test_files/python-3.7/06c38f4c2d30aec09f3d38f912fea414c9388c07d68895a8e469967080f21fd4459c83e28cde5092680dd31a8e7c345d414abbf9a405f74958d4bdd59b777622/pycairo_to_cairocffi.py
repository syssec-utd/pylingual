import cairo
import cairocffi

def _UNSAFE_pycairo_context_to_cairocffi(pycairo_context):
    if not isinstance(pycairo_context, cairo.Context):
        raise TypeError('Expected a cairo.Context, got %r' % pycairo_context)
    return cairocffi.Context._from_pointer(cairocffi.ffi.cast('cairo_t **', id(pycairo_context) + object.__basicsize__)[0], incref=True)