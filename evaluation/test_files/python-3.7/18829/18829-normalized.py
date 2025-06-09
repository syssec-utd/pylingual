def register_pyglet_handler(peng, func, event, raiseErrors=False):
    """
    Registers the given pyglet-style event handler for the given pyglet event.
    
    This function allows pyglet-style event handlers to receive events bridged
    through the peng3d event system. Internally, this function creates a lambda
    function that decodes the arguments and then calls the pyglet-style event handler.
    
    The ``raiseErrors`` flag is passed through to the peng3d event system and will
    cause any errors raised by this handler to be ignored.
    
    .. seealso::
       See :py:meth:`~peng3d.peng.Peng.addEventListener()` for more information.
    """
    peng.addEventListener('pyglet:%s' % event, lambda data: func(*data['args']), raiseErrors)