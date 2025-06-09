def main():
    """ Main *boilerplate* function to start simulation """
    logger = logging.getLogger()
    folder = os.path.join(os.getcwd(), 'experiments', 'ca_patterns_pypet')
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, 'all_patterns.hdf5')
    env = Environment(trajectory='cellular_automata', multiproc=True, ncores=4, wrap_mode='QUEUE', filename=filename, overwrite_file=True)
    traj = env.traj
    traj.par.ncells = Parameter('ncells', 400, 'Number of cells')
    traj.par.steps = Parameter('steps', 250, 'Number of timesteps')
    traj.par.rule_number = Parameter('rule_number', 30, 'The ca rule')
    traj.par.initial_name = Parameter('initial_name', 'random', 'The type of initial state')
    traj.par.seed = Parameter('seed', 100042, 'RNG Seed')
    exp_dict = {'rule_number': [10, 30, 90, 110, 184], 'initial_name': ['single', 'random']}
    exp_dict = cartesian_product(exp_dict)
    traj.f_explore(exp_dict)
    logger.info('Starting Simulation')
    env.run(wrap_automaton)
    traj.f_load(load_data=2)
    logger.info('Printing data')
    for (idx, run_name) in enumerate(traj.f_iter_runs()):
        filename = os.path.join(folder, make_filename(traj))
        plot_pattern(traj.crun.pattern, traj.rule_number, filename)
        progressbar(idx, len(traj), logger=logger)
    env.disable_logging()