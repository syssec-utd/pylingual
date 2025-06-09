def bar(self, height='thickness', sort=False, reverse=False, legend=None, ax=None, figsize=None, **kwargs):
    """
        Make a bar plot of thickness per interval.
        
        Args:
            height (str): The property of the primary component to plot.
            sort (bool or function): Either pass a boolean indicating whether
                to reverse sort by thickness, or pass a function to be used as
                the sort key.
            reverse (bool): Reverses the sort order.
            legend (Legend): The legend to plot with.
            ax (axis): Optional axis to plot to.
            figsize (tuple): A figure size, (width, height), optional.
            **kwargs: passed to the matplotlib bar plot command, ax.bar().
            
        Returns:
            axis: If you sent an axis in, you get it back.
        """
    if sort:
        if sort is True:

            def func(x):
                return x.thickness
            reverse = True
        data = sorted(self, key=func, reverse=reverse)
    else:
        data = self[:]
    if ax is None:
        (fig, ax) = plt.subplots(figsize=figsize)
    heights = [getattr(i, height) for i in data]
    comps = [i[0] for i in self.unique]
    if legend is None:
        legend = Legend.random(comps)
    colors = [legend.get_colour(i.primary) for i in data]
    bars = ax.bar(range(len(data)), height=heights, color=colors, **kwargs)
    colourables = [i.primary.summary() for i in data]
    unique_bars = dict(zip(colourables, bars))
    ax.legend(unique_bars.values(), unique_bars.keys())
    ax.set_ylabel(height.title())
    return ax