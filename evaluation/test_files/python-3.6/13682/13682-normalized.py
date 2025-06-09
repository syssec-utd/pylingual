def contains_add(self, item):
    """Takes a collection and an item and returns a new collection
    of the same type that contains the item. The notion of "contains"
    is defined by the object itself; The following must be ``True``:

    .. code-block:: python

        item in contains_add(obj, item)

    This function is used by some lenses (particularly ContainsLens)
    to add new items to containers when necessary.

    The corresponding method call for this hook is
    ``obj._lens_contains_add(item)``.

    There is no default implementation.
    """
    try:
        self._lens_contains_add
    except AttributeError:
        message = "Don't know how to add an item to {}"
        raise NotImplementedError(message.format(type(self)))
    else:
        return self._lens_contains_add(item)