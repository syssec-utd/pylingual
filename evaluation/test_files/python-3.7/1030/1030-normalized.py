def _choose_random_direction(current_state_parts, batch_rank, seed=None):
    """Chooses a random direction in the event space."""
    seed_gen = distributions.SeedStream(seed, salt='_choose_random_direction')
    rnd_direction_parts = [tf.random.normal(tf.shape(input=current_state_part), dtype=tf.float32, seed=seed_gen()) for current_state_part in current_state_parts]
    sum_squares = sum((tf.reduce_sum(input_tensor=rnd_direction ** 2.0, axis=tf.range(batch_rank, tf.rank(rnd_direction)), keepdims=True) for rnd_direction in rnd_direction_parts))
    rnd_direction_parts = [rnd_direction / tf.sqrt(sum_squares) for rnd_direction in rnd_direction_parts]
    return rnd_direction_parts