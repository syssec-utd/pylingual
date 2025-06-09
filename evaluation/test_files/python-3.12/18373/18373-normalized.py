def add_accelerator(control, key, func, id=None):
    """
 Adds a key to the control.
 
 control: The control that the accelerator should be added to.
 key: A string like "CTRL+F", or "CMD+T" that specifies the key to use.
 func: The function that should be called when key is pressed.
 id: The id to Bind the event to. Defaults to wx.NewId().
 """
    logger.debug('Adding key "%s" to control %s to call %s.', key, control, func)
    id = get_id(id)
    control.Bind(wx.EVT_MENU, func, id=id)
    t = _tables.get(control, [])
    modifiers, key_int = str_to_key(key)
    t.append((modifiers, key_int, id))
    _tables[control] = t
    update_accelerators(control)
    return id