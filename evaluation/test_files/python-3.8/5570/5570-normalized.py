def report_total_messages_stats(sect, stats, previous_stats):
    """make total errors / warnings report"""
    lines = ['type', 'number', 'previous', 'difference']
    lines += checkers.table_lines_from_stats(stats, previous_stats, ('convention', 'refactor', 'warning', 'error'))
    sect.append(report_nodes.Table(children=lines, cols=4, rheaders=1))