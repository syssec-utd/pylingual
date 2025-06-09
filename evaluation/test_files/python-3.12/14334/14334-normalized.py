def _add_to_filemenu():
    """Helper function for the above :func:add_to_filemenu()

    This function is serialised into a string and passed on
    to evalDeferred above.

    """
    import os
    import pyblish
    from maya import cmds
    for item in ('pyblishOpeningDivider', 'pyblishScene', 'pyblishCloseDivider'):
        if cmds.menuItem(item, exists=True):
            cmds.deleteUI(item, menuItem=True)
    icon = os.path.dirname(pyblish.__file__)
    icon = os.path.join(icon, 'icons', 'logo-32x32.svg')
    cmds.menuItem('pyblishOpeningDivider', divider=True, insertAfter='saveAsOptions', parent='mainFileMenu')
    cmds.menuItem('pyblishScene', insertAfter='pyblishOpeningDivider', label='Publish', parent='mainFileMenu', image=icon, command='import pyblish_maya;pyblish_maya.show()')
    cmds.menuItem('pyblishCloseDivider', insertAfter='pyblishScene', parent='mainFileMenu', divider=True)