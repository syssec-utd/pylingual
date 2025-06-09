def plot(self, legend=None, width=1.5, ladder=True, aspect=10, ticks=(1, 10), match_only=None, ax=None, return_fig=False, colour=None, cmap='viridis', default=None, style='intervals', field=None, **kwargs):
    """
        Hands-free plotting.

        Args:
            legend (Legend): The Legend to use for colours, etc.
            width (int): The width of the plot, in inches. Default 1.
            ladder (bool): Whether to use widths or not. Default False.
            aspect (int): The aspect ratio of the plot. Default 10.
            ticks (int or tuple): The (minor,major) tick interval for depth.
                Only the major interval is labeled. Default (1,10).
            match_only (list): A list of strings matching the attributes you
                want to compare when plotting.
            ax (ax): A maplotlib axis to plot onto. If you pass this, it will
                be returned. Optional.
            return_fig (bool): Whether or not to return the maplotlib ``fig``
                object. Default False.
            colour (str): Which data field to use for colours.
            cmap (cmap): Matplotlib colourmap. Default ``viridis``.
            **kwargs are passed through to matplotlib's ``patches.Rectangle``.

        Returns:
            None. Unless you specify ``return_fig=True`` or pass in an ``ax``.
        """
    if legend is None:
        legend = Legend.random(self.components)
    if style.lower() == 'tops':
        width = max([3, width])
    if ax is None:
        return_ax = False
        fig = plt.figure(figsize=(width, aspect * width))
        ax = fig.add_axes([0.35, 0.05, 0.6, 0.95])
    else:
        return_ax = True
    if self.order == 'none' or style.lower() == 'points':
        ax = self.plot_points(ax=ax, legend=legend, field=field, **kwargs)
    elif style.lower() == 'field':
        if field is None:
            raise StriplogError('You must provide a field to plot.')
        ax = self.plot_field(ax=ax, legend=legend, field=field)
    elif style.lower() == 'tops':
        ax = self.plot_tops(ax=ax, legend=legend, field=field)
        ax.set_xticks([])
    else:
        ax = self.plot_axis(ax=ax, legend=legend, ladder=ladder, default_width=width, match_only=kwargs.get('match_only', match_only), colour=colour, cmap=cmap, default=default, width_field=field, **kwargs)
        ax.set_xlim([0, width])
        ax.set_xticks([])
    lower, upper = (self[-1].base.z, self[0].top.z)
    rng = abs(upper - lower)
    ax.set_ylim([lower, upper])
    try:
        ticks = tuple(ticks)
    except TypeError:
        ticks = (1, ticks)
    while rng / ticks[0] > 250:
        mi, ma = (10 * ticks[0], ticks[1])
        if ma <= mi:
            ma = 10 * mi
        ticks = (mi, ma)
    minorLocator = mpl.ticker.MultipleLocator(ticks[0])
    ax.yaxis.set_minor_locator(minorLocator)
    majorLocator = mpl.ticker.MultipleLocator(ticks[1])
    majorFormatter = mpl.ticker.FormatStrFormatter('%d')
    ax.yaxis.set_major_locator(majorLocator)
    ax.yaxis.set_major_formatter(majorFormatter)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.get_yaxis().set_tick_params(which='both', direction='out')
    title = getattr(self, 'title', None)
    if title is not None:
        ax.set_title(title)
    ax.patch.set_alpha(0)
    if return_ax:
        return ax
    elif return_fig:
        return fig
    else:
        return