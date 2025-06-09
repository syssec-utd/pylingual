def add_exploration(traj):
    """Explores different values of `I` and `tau_ref`."""
    print('Adding exploration of I and tau_ref')
    explore_dict = {'neuron.I': np.arange(0, 1.01, 0.01).tolist(), 'neuron.tau_ref': [5.0, 7.5, 10.0]}
    explore_dict = cartesian_product(explore_dict, ('neuron.tau_ref', 'neuron.I'))
    traj.f_explore(explore_dict)