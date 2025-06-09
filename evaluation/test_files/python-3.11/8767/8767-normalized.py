def show_progress(job):
    """
    This utility function will print the progress of a passed iterator job as
    started by ``refresh_indices()`` and ``clean_old_index()``.

    Usage example::

        class RomTest(Model):
            pass

        for i in xrange(1000):
            RomTest().save()

        util.show_progress(util.clean_old_index(RomTest))
    """
    start = time.time()
    last_print = 0
    last_line = 0
    for prog, total in chain(job, [(1, 1)]):
        if time.time() - last_print > 0.1 or prog >= total:
            delta = time.time() - start or 0.0001
            line = '%.1f%% complete, %.1f seconds elapsed, %.1f seconds remaining' % (100.0 * prog / (total or 1), delta, total * delta / (prog or 1) - delta)
            length = len(line)
            line += max(last_line - length, 0) * ' '
            print(line, end='\r')
            last_line = length
            last_print = time.time()
    print()