def get(self):
    """Return current profiler statistics."""
    sort = self.get_argument('sort', 'cum_time')
    count = self.get_argument('count', 20)
    strip_dirs = self.get_argument('strip_dirs', True)
    error = ''
    sorts = ('num_calls', 'cum_time', 'total_time', 'cum_time_per_call', 'total_time_per_call')
    if sort not in sorts:
        error += "Invalid `sort` '%s', must be in %s." % (sort, sorts)
    try:
        count = int(count)
    except (ValueError, TypeError):
        error += "Can't cast `count` '%s' to int." % count
    if count <= 0:
        count = None
    strip_dirs = str(strip_dirs).lower() not in ('false', 'no', 'none', 'null', '0', '')
    if error:
        self.write({'error': error})
        self.set_status(400)
        self.finish()
        return
    try:
        statistics = get_profiler_statistics(sort, count, strip_dirs)
        self.write({'statistics': statistics})
        self.set_status(200)
    except TypeError:
        logger.exception('Error while retrieving profiler statistics')
        self.write({'error': 'No stats available. Start and stop the profiler before trying to retrieve stats.'})
        self.set_status(404)
    self.finish()