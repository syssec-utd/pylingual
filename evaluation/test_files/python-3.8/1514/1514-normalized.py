def _batch_interp_with_gather_nd(x, x_ref_min, x_ref_max, y_ref, nd, fill_value, batch_dims):
    """N-D interpolation that works with leading batch dims."""
    dtype = x.dtype
    ny = tf.cast(tf.shape(input=y_ref)[batch_dims:batch_dims + nd], dtype)
    x_ref_min_expanded = tf.expand_dims(x_ref_min, axis=-2)
    x_ref_max_expanded = tf.expand_dims(x_ref_max, axis=-2)
    x_idx_unclipped = (ny - 1) * (x - x_ref_min_expanded) / (x_ref_max_expanded - x_ref_min_expanded)
    nan_idx = tf.math.is_nan(x_idx_unclipped)
    x_idx_unclipped = tf.where(nan_idx, tf.zeros_like(x_idx_unclipped), x_idx_unclipped)
    x_idx = tf.clip_by_value(x_idx_unclipped, tf.zeros((), dtype=dtype), ny - 1)
    idx_below = tf.floor(x_idx)
    idx_above = tf.minimum(idx_below + 1, ny - 1)
    idx_below = tf.maximum(idx_above - 1, 0)
    idx_below_int32 = tf.cast(idx_below, dtype=tf.int32)
    idx_above_int32 = tf.cast(idx_above, dtype=tf.int32)
    idx_below_list = tf.unstack(idx_below_int32, axis=-1)
    idx_above_list = tf.unstack(idx_above_int32, axis=-1)
    t = x_idx - idx_below

    def _expand_x_fn(tensor):
        extended_shape = tf.concat([tf.shape(input=tensor), tf.ones_like(tf.shape(input=y_ref)[batch_dims + nd:])], axis=0)
        return tf.reshape(tensor, extended_shape)
    t = _expand_x_fn(t)
    s = 1 - t
    nan_idx = _expand_x_fn(nan_idx)
    t = tf.where(nan_idx, tf.fill(tf.shape(input=t), tf.constant(np.nan, dtype)), t)
    terms = []
    for zero_ones_list in _binary_count(nd):
        gather_from_y_ref_idx = []
        opposite_volume_t_idx = []
        opposite_volume_s_idx = []
        for (k, zero_or_one) in enumerate(zero_ones_list):
            if zero_or_one == 0:
                gather_from_y_ref_idx.append(idx_below_list[k])
                opposite_volume_s_idx.append(k)
            else:
                gather_from_y_ref_idx.append(idx_above_list[k])
                opposite_volume_t_idx.append(k)
        ov_axis = tf.rank(x) - 1
        opposite_volume = tf.reduce_prod(input_tensor=tf.gather(t, indices=tf.cast(opposite_volume_t_idx, dtype=tf.int32), axis=ov_axis), axis=ov_axis) * tf.reduce_prod(input_tensor=tf.gather(s, indices=tf.cast(opposite_volume_s_idx, dtype=tf.int32), axis=ov_axis), axis=ov_axis)
        y_ref_pt = tf.gather_nd(y_ref, tf.stack(gather_from_y_ref_idx, axis=-1), batch_dims=batch_dims)
        terms.append(y_ref_pt * opposite_volume)
    y = tf.math.add_n(terms)
    if tf.debugging.is_numeric_tensor(fill_value):
        oob_idx = tf.reduce_any(input_tensor=(x_idx_unclipped < 0) | (x_idx_unclipped > ny - 1), axis=-1)
        oob_idx = _expand_x_fn(oob_idx)
        oob_idx |= tf.fill(tf.shape(input=y), False)
        y = tf.where(oob_idx, tf.fill(tf.shape(input=y), fill_value), y)
    return y