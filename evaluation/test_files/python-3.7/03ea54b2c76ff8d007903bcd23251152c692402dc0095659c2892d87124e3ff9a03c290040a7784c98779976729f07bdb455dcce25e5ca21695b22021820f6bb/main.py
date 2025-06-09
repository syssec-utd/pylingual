import matplotlib.pyplot as plt
import seaborn as sns
from .plotsize import Sizing
from .configuration import BackendConfiguration
from .utils import set_text, save, copy_docstring

class Plotex:
    """
    a facade over various different functions in the module for a direct one-point access
    """

    def __init__(self, **kwargs):
        """
        initialize the controller

        :param kwargs: parameters for the config file, the params include `url`         (the url for the config file), `cmap/palette` for the cmap, `style/theme`
        for the seaborn style
        """
        self.config = BackendConfiguration(**kwargs)
        self.sizer = Sizing(config=self.config)
        self.params = None
        self.config.initialize()

    def skeleton(self, width=None, publisher=None, width_in_pts=True, reinitialize=True, fraction=1, subplots=(1, 1), **kwargs):
        """
        finds the ideal size of the plot and adjusts the text sizes according to the required dimensions
        this is a dummy function wrapped over the `get_figure` function from Sizing to enable direct access

        :param width: the width, defaults to None
        :param publisher: the name of the publisher, defaults to None
        :param width_in_pts: whether the width is in points, defaults to True
        :param reinitialize: whether to reinitialize the config to itys defaults, defaults to True
        :param fraction: the fraction of the width supplied to use, defaults to 1
        :param subplots: (nrows, ncols), defaults to (1, 1)
        
        :return: fig, axes if return_size is False, else (width, height)
        """
        output = self.sizer.get_size(width=width, publisher=publisher, width_in_pts=width_in_pts, reinitialize=reinitialize, fraction=fraction, subplots=subplots, **kwargs)
        self.params = plt.rcParams.copy()
        return output

    def update_textsize(self, reinitialize=True, **kwargs):
        """
        This function changes the font size of various text elements in the plot such as xlabel,         ylabel, title, ticks, etc., by a specified offset. Uses deterministic and probabilistic         matching to determine and map the keyword argument to the required property
        
        :param reinitialize: initialize size params to those created by `get_size` after adjusting for            columns, fraction etc.
        :param kwargs: flexible keyword arguments specified by the user, where the name of         the argument is the key and the offset is the value.
        """
        self.sizer.update_textsize(reinitialize=reinitialize, **kwargs)

    def update_textweight(self, reinitialize=False, **kwargs):
        """
        This function changes the font weight of various text elements in the plot such as xlabel,         ylabel, title. The values are 'light', 'normal', 'bold'.
        Uses deterministic and probabilistic matching to determine and map the keyword 
        \\ argument to the required property
        
        :param reinitialize: initialize size params to those created by `get_size` after adjusting for            columns, fraction etc.
        :param kwargs: flexible keyword arguments specified by the user, where the name of         the argument is the key and the weight is the value.
        """
        self.sizer.update_textweight(reinitialize=reinitialize, **kwargs)

    def remove_ticks(self, xtick=True, ytick=True):
        """
        remove the tick marks 

        :param xtick: remove ticks on x-axis, defaults to True
        :param ytick: remove ticks on y-axis, defaults to True
        """
        self.sizer.remove_ticks(xtick=xtick, ytick=ytick)

    def set_lim(self, ax, xlims=(None, None), ylims=(None, None)):
        """
        set the starting and ending points of the x and y axes

        :param ax: the matplotlib axis object
        :param xlims: tuple containing the (min, max) values of the                         x axis, defaults to (None, None)
        :param ylims: tuple containing the (min, max) values of the                         y axis, defaults to (None, None)
        """
        if xlims[0] is not None and xlims[1] is not None:
            ax.set_xlim(xlims[0], xlims[1])
        if ylims[0] is not None and ylims[1] is not None:
            ax.set_ylim(ylims[0], ylims[1])

    @copy_docstring(set_text)
    def set_text(self, plt=None, ax=None, xlabel=None, ylabel=None, title=None, xticklocs=None, xticklabels=None, xtickrot=None, yticklocs=None, yticklabels=None, ytickrot=None):
        set_text(plt=plt, ax=ax, xlabel=xlabel, ylabel=ylabel, title=title, xticklocs=xticklocs, xticklabels=xticklabels, xtickrot=xtickrot, yticklocs=yticklocs, yticklabels=yticklabels, ytickrot=ytickrot)

    @copy_docstring(save)
    def save(self, save_path, fig=None, plt=None, format='pdf'):
        save(save_path, fig=fig, plt=plt, format=format)