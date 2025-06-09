def _format_heatmap(self, filename, heatmap, execution_count):
    """Formats heatmap for UI."""
    with open(filename) as src_file:
        file_source = src_file.read().split('\n')
        skip_map = self._calc_skips(heatmap, len(file_source))
    run_time = sum((time for time in heatmap.values()))
    return {'name': filename, 'heatmap': heatmap, 'executionCount': execution_count, 'srcCode': self._skip_lines(file_source, skip_map), 'runTime': run_time}