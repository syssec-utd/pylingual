def plot(self, fmt=None, fig=None, ax=None):
    """
        Make a simple plot of the Decor.

        Args:
            fmt (str): A Python format string for the component summaries.
            fig (Pyplot figure): A figure, optional. Use either fig or ax, not
                both.
            ax (Pyplot axis): An axis, optional. Use either fig or ax, not
                both.

        Returns:
            fig or ax or None. If you pass in an ax, you get it back. If you pass
                in a fig, you get it. If you pass nothing, the function creates a
                plot object as a side-effect.
        """
    u = 4
    v = 0.25
    r = None
    if fig is None and ax is None:
        fig = plt.figure(figsize=(u, 1))
    else:
        r = fig
    if ax is None:
        ax = fig.add_axes([0.1 * v, 0.1, 0.8 * v, 0.8])
    else:
        r = ax
    rect1 = patches.Rectangle((0, 0), u * v, u * v, color=self.colour, lw=1, hatch=self.hatch, ec='k')
    ax.add_patch(rect1)
    ax.text(1.0 + 0.1 * v * u, u * v * 0.5, self.component.summary(fmt=fmt), fontsize=max(u, 15), verticalalignment='center', horizontalalignment='left')
    ax.set_xlim([0, u * v])
    ax.set_ylim([0, u * v])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.invert_yaxis()
    return r