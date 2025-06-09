def _score_step(step):
    """Count the mapped two-qubit gates, less the number of added SWAPs."""
    return len([g for g in step['gates_mapped'] if len(g.qargs) == 2]) - 3 * step['swaps_added']