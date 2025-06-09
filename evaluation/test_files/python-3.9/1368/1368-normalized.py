def kalman_transition(filtered_mean, filtered_cov, transition_matrix, transition_noise):
    """Propagate a filtered distribution through a transition model."""
    predicted_mean = _propagate_mean(filtered_mean, transition_matrix, transition_noise)
    predicted_cov = _propagate_cov(filtered_cov, transition_matrix, transition_noise)
    return (predicted_mean, predicted_cov)