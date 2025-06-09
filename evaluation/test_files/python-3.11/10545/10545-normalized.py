def _assess_resource_warnings(self, process, vals):
    """Assess whether the cpu load or memory usage is above the allocation

        Parameters
        ----------
        process : str
            Process name
        vals : vals
            List of trace information for each tag of that process

        Returns
        -------
        cpu_warnings : dict
            Keys are tags and values are the excessive cpu load
        mem_warnings : dict
            Keys are tags and values are the excessive rss
        """
    cpu_warnings = {}
    mem_warnings = {}
    for i in vals:
        try:
            expected_load = float(i['cpus']) * 100
            cpu_load = float(i['%cpu'].replace(',', '.').replace('%', ''))
            if expected_load * 0.9 > cpu_load > expected_load * 1.1:
                cpu_warnings[i['tag']] = {'expected': expected_load, 'value': cpu_load}
        except (ValueError, KeyError):
            pass
        try:
            rss = self._size_coverter(i['rss'])
            mem_allocated = self._size_coverter(i['memory'])
            if rss > mem_allocated * 1.1:
                mem_warnings[i['tag']] = {'expected': mem_allocated, 'value': rss}
        except (ValueError, KeyError):
            pass
    return (cpu_warnings, mem_warnings)