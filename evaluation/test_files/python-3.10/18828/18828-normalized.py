def patch_float2int():
    """
    Patches the :py:mod:`pyglet.graphics.vertexattribute`\\ , :py:mod:`pyglet.graphics.vertexbuffer` and :py:mod:`pyglet.graphics.vertexdomain` modules.
    
    This patch is only needed with Python 3.x and will be applied automatically when initializing :py:class:`Peng()`\\ .
    
    The patches consist of simply converting some list indices, slices and other numbers to integers from floats with .0. These patches have not been tested thoroughly, but work with at least ``test.py`` and ``test_gui.py``\\ .
    
    Can be enabled and disabled via :confval:`pyglet.patch.patch_float2int`\\ .
    """
    pyglet.graphics.vertexattribute.AbstractAttribute.get_region = _get_region
    pyglet.graphics.vertexbuffer.MappableVertexBufferObject.bind = _bind
    pyglet.graphics.vertexbuffer.IndirectArrayRegion.__setitem__ = _iar__setitem__
    pyglet.graphics.vertexdomain.VertexDomain.draw = _draw