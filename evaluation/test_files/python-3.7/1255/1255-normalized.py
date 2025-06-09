def _assert_same_base_type(items, expected_type=None):
    """Asserts all items are of the same base type.

  Args:
    items: List of graph items (e.g., `Variable`, `Tensor`, `SparseTensor`,
        `Operation`, or `IndexedSlices`). Can include `None` elements, which
        will be ignored.
    expected_type: Expected type. If not specified, assert all items are
        of the same base type.

  Returns:
    Validated type, or none if neither expected_type nor items provided.

  Raises:
    ValueError: If any types do not match.
  """
    original_expected_type = expected_type
    mismatch = False
    for item in items:
        if item is not None:
            item_type = base_dtype(item.dtype)
            if not expected_type:
                expected_type = item_type
            elif expected_type != item_type:
                mismatch = True
                break
    if mismatch:
        expected_type = original_expected_type
        original_item_str = None
        get_name = lambda x: x.name if hasattr(x, 'name') else str(x)
        for item in items:
            if item is not None:
                item_type = base_dtype(item.dtype)
                if not expected_type:
                    expected_type = item_type
                    original_item_str = get_name(item)
                elif expected_type != item_type:
                    raise ValueError('{}, type={}, must be of the same type ({}){}.'.format(get_name(item), item_type, expected_type, ' as {}'.format(original_item_str) if original_item_str else ''))
        return expected_type
    else:
        return expected_type