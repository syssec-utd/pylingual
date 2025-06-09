def add_parameters(traj):
    """Adds all neuron group parameters to `traj`."""
    assert isinstance(traj, Trajectory)
    traj.v_standard_parameter = Brian2Parameter
    scale = traj.simulation.scale
    traj.f_add_parameter('connections.R_ee', 1.0, comment='Scaling factor for clustering')
    traj.f_add_parameter('connections.clustersize_e', 100, comment='Size of a cluster')
    traj.f_add_parameter('connections.strength_factor', 2.5, comment='Factor for scaling cluster weights')
    traj.f_add_parameter('connections.p_ii', 0.25, comment='Connection probability from inhibitory to inhibitory')
    traj.f_add_parameter('connections.p_ei', 0.25, comment='Connection probability from inhibitory to excitatory')
    traj.f_add_parameter('connections.p_ie', 0.25, comment='Connection probability from excitatory to inhibitory')
    traj.f_add_parameter('connections.p_ee', 0.1, comment='Connection probability from excitatory to excitatory')
    traj.f_add_parameter('connections.J_ii', 0.027 / np.sqrt(scale), comment='Connection strength from inhibitory to inhibitory')
    traj.f_add_parameter('connections.J_ei', 0.032 / np.sqrt(scale), comment='Connection strength from inhibitory to excitatroy')
    traj.f_add_parameter('connections.J_ie', 0.009 / np.sqrt(scale), comment='Connection strength from excitatory to inhibitory')
    traj.f_add_parameter('connections.J_ee', 0.012 / np.sqrt(scale), comment='Connection strength from excitatory to excitatory')