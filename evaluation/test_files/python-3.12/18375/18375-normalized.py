def add_hotkey(control, key, func, id=None):
    """
 Add a global hotkey bound to control via id that should call func.
 
 control: The control to bind to.
 key: The hotkey to use.
 func: The func to call.
 id: The new ID to use (defaults to creating a new ID.
 """
    if win32con is None:
        raise RuntimeError('win32con is not available.')
    logger.debug('Adding hotkey "%s" to control %s to call %s.', key, control, func)
    modifiers, keycode = str_to_key(key, key_table=win32con, accel_format='MOD_%s', key_format='VK_%s', key_transpositions={'CTRL': 'CONTROL'})
    id = get_id(id)
    control.Bind(wx.EVT_HOTKEY, func, id=id)
    l = _hotkeys.get(control, [])
    l.append([key, id])
    _hotkeys[control] = l
    return control.RegisterHotKey(id, modifiers, keycode)