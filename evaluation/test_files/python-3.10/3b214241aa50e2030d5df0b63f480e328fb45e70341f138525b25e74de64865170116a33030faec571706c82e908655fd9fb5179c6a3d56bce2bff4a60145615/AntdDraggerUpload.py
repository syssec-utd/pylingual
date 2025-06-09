from dash.development.base_component import Component, _explicitize_args

class AntdDraggerUpload(Component):
    """An AntdDraggerUpload component.


Keyword arguments:

- id (string; optional)

- apiUrl (string; optional)

- className (string | dict; optional)

- defaultFileList (list of dicts; optional)

    `defaultFileList` is a list of dicts with keys:

    - name (string; optional)

    - status (a value equal to: 'done', 'error', 'removed'; optional)

    - uid (boolean | number | string | dict | list; optional)

    - url (string; optional)

- directory (boolean; optional)

- downloadUrl (string; optional)

- draggerClassName (string | dict; optional)

- draggerStyle (dict; optional)

- failedTooltipInfo (string; optional)

- fileListMaxLength (number; optional)

- fileMaxSize (number; default 500)

- fileTypes (list of strings; optional)

- hint (string; optional)

- key (string; optional)

- lastUploadTaskRecord (dict; optional)

    `lastUploadTaskRecord` is a dict with keys:

    - completeTimestamp (number; optional)

    - fileName (string; optional)

    - fileSize (number; optional)

    - taskId (string; optional)

    - taskStatus (string; optional) | list of dicts with keys:

    - completeTimestamp (number; optional)

    - fileName (string; optional)

    - fileSize (number; optional)

    - taskId (string; optional)

    - taskStatus (string; optional)

- listUploadTaskRecord (dict; optional)

    `listUploadTaskRecord` is a dict with keys:

    - completeTimestamp (number; optional)

    - fileName (string; optional)

    - fileSize (number; optional)

    - taskId (string; optional)

    - taskStatus (string; optional)

    - uid (string; optional)

    - url (string; optional) | list of dicts with keys:

    - completeTimestamp (number; optional)

    - fileName (string; optional)

    - fileSize (number; optional)

    - taskId (string; optional)

    - taskStatus (string; optional)

    - uid (string; optional)

    - url (string; optional)

- loading_state (dict; optional)

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- locale (a value equal to: 'zh-cn', 'en-us'; default 'zh-cn')

- multiple (boolean; optional)

- showUploadList (boolean; optional)

- status (a value equal to: 'error', 'warning'; optional)

- style (dict; optional)

- text (string; optional)

- uploadId (string; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dmp_dash_components'
    _type = 'AntdDraggerUpload'

    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, draggerClassName=Component.UNDEFINED, draggerStyle=Component.UNDEFINED, key=Component.UNDEFINED, locale=Component.UNDEFINED, apiUrl=Component.UNDEFINED, downloadUrl=Component.UNDEFINED, text=Component.UNDEFINED, hint=Component.UNDEFINED, fileListMaxLength=Component.UNDEFINED, fileTypes=Component.UNDEFINED, uploadId=Component.UNDEFINED, fileMaxSize=Component.UNDEFINED, multiple=Component.UNDEFINED, directory=Component.UNDEFINED, failedTooltipInfo=Component.UNDEFINED, showUploadList=Component.UNDEFINED, lastUploadTaskRecord=Component.UNDEFINED, listUploadTaskRecord=Component.UNDEFINED, defaultFileList=Component.UNDEFINED, status=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'apiUrl', 'className', 'defaultFileList', 'directory', 'downloadUrl', 'draggerClassName', 'draggerStyle', 'failedTooltipInfo', 'fileListMaxLength', 'fileMaxSize', 'fileTypes', 'hint', 'key', 'lastUploadTaskRecord', 'listUploadTaskRecord', 'loading_state', 'locale', 'multiple', 'showUploadList', 'status', 'style', 'text', 'uploadId']
        self._valid_wildcard_attributes = []
        self.available_properties = ['id', 'apiUrl', 'className', 'defaultFileList', 'directory', 'downloadUrl', 'draggerClassName', 'draggerStyle', 'failedTooltipInfo', 'fileListMaxLength', 'fileMaxSize', 'fileTypes', 'hint', 'key', 'lastUploadTaskRecord', 'listUploadTaskRecord', 'loading_state', 'locale', 'multiple', 'showUploadList', 'status', 'style', 'text', 'uploadId']
        self.available_wildcard_properties = []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)
        args = {k: _locals[k] for k in _explicit_args}
        super(AntdDraggerUpload, self).__init__(**args)