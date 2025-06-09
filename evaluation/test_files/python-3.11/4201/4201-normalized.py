def config_tab(backend):
    """The backend configuration widget.

    Args:
        backend (IBMQbackend): The backend.

    Returns:
        grid: A GridBox widget.
    """
    status = backend.status().to_dict()
    config = backend.configuration().to_dict()
    config_dict = {**status, **config}
    upper_list = ['n_qubits', 'operational', 'status_msg', 'pending_jobs', 'basis_gates', 'local', 'simulator']
    lower_list = list(set(config_dict.keys()).difference(upper_list))
    lower_list.remove('gates')
    upper_str = '<table>'
    upper_str += '<style>\ntable {\n    border-collapse: collapse;\n    width: auto;\n}\n\nth, td {\n    text-align: left;\n    padding: 8px;\n}\n\ntr:nth-child(even) {background-color: #f6f6f6;}\n</style>'
    footer = '</table>'
    upper_str += '<tr><th>Property</th><th>Value</th></tr>'
    for key in upper_list:
        upper_str += "<tr><td><font style='font-weight:bold'>%s</font></td><td>%s</td></tr>" % (key, config_dict[key])
    upper_str += footer
    upper_table = widgets.HTML(value=upper_str, layout=widgets.Layout(width='100%', grid_area='left'))
    image_widget = widgets.Output(layout=widgets.Layout(display='flex-inline', grid_area='right', padding='10px 10px 10px 10px', width='auto', max_height='300px', align_items='center'))
    if not config['simulator']:
        with image_widget:
            gate_map = plot_gate_map(backend)
            display(gate_map)
        plt.close(gate_map)
    lower_str = '<table>'
    lower_str += '<style>\ntable {\n    border-collapse: collapse;\n    width: auto;\n}\n\nth, td {\n    text-align: left;\n    padding: 8px;\n}\n\ntr:nth-child(even) {background-color: #f6f6f6;}\n</style>'
    lower_str += '<tr><th></th><th></th></tr>'
    for key in lower_list:
        if key != 'name':
            lower_str += '<tr><td>%s</td><td>%s</td></tr>' % (key, config_dict[key])
    lower_str += footer
    lower_table = widgets.HTML(value=lower_str, layout=widgets.Layout(width='auto', grid_area='bottom'))
    grid = widgets.GridBox(children=[upper_table, image_widget, lower_table], layout=widgets.Layout(grid_template_rows='auto auto', grid_template_columns='25% 25% 25% 25%', grid_template_areas='\n                               "left right right right"\n                               "bottom bottom bottom bottom"\n                               ', grid_gap='0px 0px'))
    return grid