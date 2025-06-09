def add_parameters(traj):
    """Adds all necessary parameters to the `traj` container.

    You can choose between two parameter sets. One for the Lorenz attractor and
    one for the Roessler attractor.
    The former is chosen for `traj.diff_name=='diff_lorenz'`, the latter for
    `traj.diff_name=='diff_roessler'`.
    You can use parameter presetting to switch between the two cases.

    :raises: A ValueError if `traj.diff_name` is none of the above

    """
    traj.f_add_parameter('steps', 10000, comment='Number of time steps to simulate')
    traj.f_add_parameter('dt', 0.01, comment='Step size')
    traj.f_add_parameter(ArrayParameter, 'initial_conditions', np.array([0.0, 0.0, 0.0]), comment='Our initial conditions, as default we will start from origin!')
    traj.f_add_parameter('diff_name', 'diff_lorenz', comment='Name of our differential equation')
    if traj.diff_name == 'diff_lorenz':
        traj.f_add_parameter('func_params.sigma', 10.0)
        traj.f_add_parameter('func_params.beta', 8.0 / 3.0)
        traj.f_add_parameter('func_params.rho', 28.0)
    elif traj.diff_name == 'diff_roessler':
        traj.f_add_parameter('func_params.a', 0.1)
        traj.f_add_parameter('func_params.c', 14.0)
    else:
        raise ValueError("I don't know what %s is." % traj.diff_name)