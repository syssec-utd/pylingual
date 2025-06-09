def _prepare_args_with_initial_vertex(objective_function, initial_vertex, step_sizes, objective_at_initial_vertex, batch_evaluate_objective):
    """Constructs a standard axes aligned simplex."""
    dim = tf.size(input=initial_vertex)
    num_vertices = dim + 1
    unit_vectors_along_axes = tf.reshape(tf.eye(dim, dim, dtype=initial_vertex.dtype.base_dtype), tf.concat([[dim], tf.shape(input=initial_vertex)], axis=0))
    simplex_face = initial_vertex + step_sizes * unit_vectors_along_axes
    simplex = tf.concat([tf.expand_dims(initial_vertex, axis=0), simplex_face], axis=0)
    num_evaluations = 0
    if objective_at_initial_vertex is None:
        objective_at_initial_vertex = objective_function(initial_vertex)
        num_evaluations += 1
    (objective_at_simplex_face, num_evals) = _evaluate_objective_multiple(objective_function, simplex_face, batch_evaluate_objective)
    num_evaluations += num_evals
    objective_at_simplex = tf.concat([tf.expand_dims(objective_at_initial_vertex, axis=0), objective_at_simplex_face], axis=0)
    return (dim, num_vertices, simplex, objective_at_simplex, num_evaluations)