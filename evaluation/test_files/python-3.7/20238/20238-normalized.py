def ajax_editable_boolean(attr, short_description):
    """
    Convenience function: Assign the return value of this method to a variable
    of your ModelAdmin class and put the variable name into list_display.

    Example::

        class MyTreeEditor(TreeEditor):
            list_display = ('__unicode__', 'active_toggle')

            active_toggle = ajax_editable_boolean('active', _('is active'))
    """

    def _fn(self, item):
        return ajax_editable_boolean_cell(item, attr)
    _fn.allow_tags = True
    _fn.short_description = short_description
    _fn.editable_boolean_field = attr
    return _fn