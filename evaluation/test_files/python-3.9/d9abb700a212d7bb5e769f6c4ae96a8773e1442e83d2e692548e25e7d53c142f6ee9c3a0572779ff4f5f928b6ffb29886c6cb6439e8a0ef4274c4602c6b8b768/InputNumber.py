from dash.development.base_component import Component, _explicitize_args

class InputNumber(Component):
    """An InputNumber component.
InputNumber

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- addon_after (string; optional):
    The label text displayed after (on the right side of) the input
    field.

- addon_before (string; optional):
    The label text displayed before (on the left side of) the input
    field.

- bordered (boolean; optional):
    Whether has border style.

- class_name (string; optional):
    Often used with CSS to style elements with common properties.

- controls (boolean; optional):
    Whether to show +- controls.

- debounce (boolean; default False):
    If True, changes to input will be sent back to the Dash server
    only when the enter key is pressed or when the component loses
    focus.  If it's False, it will sent the value back on every
    change.

- disabled (boolean; optional):
    Whether the input is disabled.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; required):
        Holds the name of the component that is loading.

    - is_loading (boolean; required):
        Determines if the component is loading or not.

    - prop_name (string; required):
        Holds which property is loading.

- max (number; optional):
    The max value.

- min (number; optional):
    The min value.

- n_blur (number; default 0):
    Number of times the input lost focus.

- n_blur_timestamp (number; default -1):
    Last time the input lost focus.

- n_submit (number; default 0):
    Number of times the `Enter` key was pressed while the input had
    focus.

- n_submit_timestamp (number; default -1):
    Last time that `Enter` was pressed.

- precision (number; optional):
    The precision of input value.

- prefix (string; optional):
    The prefix icon for the Input.

- read_only (boolean; optional):
    If readonly the input.

- size (a value equal to: 'large', 'middle', 'small'; optional):
    The height of input box.

- status (a value equal to: 'error', 'warning'; optional):
    Set validation status.

- step (string | number; default 1):
    The number to which the current value is increased or decreased.
    It can be an integer or decimal.

- string_mode (boolean; optional):
    Set value as string to support high precision decimals.

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- value (number; default 0):
    The current value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_antd'
    _type = 'InputNumber'

    @_explicitize_args
    def __init__(self, addon_after=Component.UNDEFINED, addon_before=Component.UNDEFINED, bordered=Component.UNDEFINED, controls=Component.UNDEFINED, debounce=Component.UNDEFINED, disabled=Component.UNDEFINED, max=Component.UNDEFINED, min=Component.UNDEFINED, precision=Component.UNDEFINED, read_only=Component.UNDEFINED, status=Component.UNDEFINED, prefix=Component.UNDEFINED, size=Component.UNDEFINED, step=Component.UNDEFINED, string_mode=Component.UNDEFINED, value=Component.UNDEFINED, n_blur=Component.UNDEFINED, n_blur_timestamp=Component.UNDEFINED, n_submit=Component.UNDEFINED, n_submit_timestamp=Component.UNDEFINED, loading_state=Component.UNDEFINED, id=Component.UNDEFINED, key=Component.UNDEFINED, style=Component.UNDEFINED, class_name=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'addon_after', 'addon_before', 'bordered', 'class_name', 'controls', 'debounce', 'disabled', 'key', 'loading_state', 'max', 'min', 'n_blur', 'n_blur_timestamp', 'n_submit', 'n_submit_timestamp', 'precision', 'prefix', 'read_only', 'size', 'status', 'step', 'string_mode', 'style', 'value']
        self._valid_wildcard_attributes = []
        self.available_properties = ['id', 'addon_after', 'addon_before', 'bordered', 'class_name', 'controls', 'debounce', 'disabled', 'key', 'loading_state', 'max', 'min', 'n_blur', 'n_blur_timestamp', 'n_submit', 'n_submit_timestamp', 'precision', 'prefix', 'read_only', 'size', 'status', 'step', 'string_mode', 'style', 'value']
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)
        args = {k: _locals[k] for k in _explicit_args}
        super(InputNumber, self).__init__(**args)