def create_character(skin, hair, top, pants):
    """Creates a character sprite from a set of attribute sprites."""
    dtype = skin.dtype
    hair_mask = tf.cast(hair[..., -1:] <= 0, dtype)
    top_mask = tf.cast(top[..., -1:] <= 0, dtype)
    pants_mask = tf.cast(pants[..., -1:] <= 0, dtype)
    char = skin * hair_mask + hair
    char = char * top_mask + top
    char = char * pants_mask + pants
    return char