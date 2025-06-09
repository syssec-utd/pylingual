from dash.development.base_component import Component, _explicitize_args

class CycleBreaker(Component):
    """A CycleBreaker component.
Simple data store that automatically copies the current value of the src property into dst property. Can be used to break circular dependencies.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- dst (boolean | number | string | dict | list; optional):
    Read the forwarded value from this property.

- src (boolean | number | string | dict | list; optional):
    Set this property to value to be forwarded from ."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_extensions'
    _type = 'CycleBreaker'

    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, src=Component.UNDEFINED, dst=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'dst', 'src']
        self._valid_wildcard_attributes = []
        self.available_properties = ['id', 'dst', 'src']
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)
        args = {k: _locals[k] for k in _explicit_args}
        super(CycleBreaker, self).__init__(**args)