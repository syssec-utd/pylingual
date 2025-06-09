def get_output_files_layout(output_category):
    """
    Parameters
    ----------
    output_category: str
        inputs: epw, idf
        table: summary table
        other: other
    """
    if output_category not in ('inputs', 'table', 'other'):
        raise RuntimeError(f'unknown {output_category}')
    layouts = _layouts_matrix[OS_NAME][output_category]
    return get_value_by_version(layouts)