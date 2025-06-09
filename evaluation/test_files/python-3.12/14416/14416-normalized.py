def process_hv_plots(widgets, plots):
    """
    Temporary fix to patch HoloViews plot comms
    """
    bokeh_plots = []
    for plot in plots:
        if hasattr(plot, '_update_callbacks'):
            for subplot in plot.traverse(lambda x: x):
                subplot.comm = widgets.server_comm
                for cb in subplot.callbacks:
                    for c in cb.callbacks:
                        c.code = c.code.replace(plot.id, widgets.plot_id)
            plot = plot.state
        bokeh_plots.append(plot)
    return bokeh_plots