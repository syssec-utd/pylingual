"""
Matplotlib GUI progressbar decorator for iterators.

Usage:
>>> from tqdm.gui import trange, tqdm
>>> for i in trange(10):
...     ...
"""
import re
from warnings import warn
from .std import TqdmExperimentalWarning
from .std import tqdm as std_tqdm
__author__ = {'github.com/': ['casperdcl', 'lrq3000']}
__all__ = ['tqdm_gui', 'tgrange', 'tqdm', 'trange']

class tqdm_gui(std_tqdm):
    """Experimental Matplotlib GUI version of tqdm!"""

    def __init__(self, *args, **kwargs):
        from collections import deque
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        kwargs = kwargs.copy()
        kwargs['gui'] = True
        colour = kwargs.pop('colour', 'g')
        super(tqdm_gui, self).__init__(*args, **kwargs)
        if self.disable:
            return
        warn('GUI is experimental/alpha', TqdmExperimentalWarning, stacklevel=2)
        self.mpl = mpl
        self.plt = plt
        self.toolbar = self.mpl.rcParams['toolbar']
        self.mpl.rcParams['toolbar'] = 'None'
        self.mininterval = max(self.mininterval, 0.5)
        self.fig, ax = plt.subplots(figsize=(9, 2.2))
        total = self.__len__()
        if total is not None:
            self.xdata = []
            self.ydata = []
            self.zdata = []
        else:
            self.xdata = deque([])
            self.ydata = deque([])
            self.zdata = deque([])
        self.line1, = ax.plot(self.xdata, self.ydata, color='b')
        self.line2, = ax.plot(self.xdata, self.zdata, color='k')
        ax.set_ylim(0, 0.001)
        if total is not None:
            ax.set_xlim(0, 100)
            ax.set_xlabel('percent')
            self.fig.legend((self.line1, self.line2), ('cur', 'est'), loc='center right')
            self.hspan = plt.axhspan(0, 0.001, xmin=0, xmax=0, color=colour)
        else:
            ax.set_xlim(0, 60)
            ax.invert_xaxis()
            ax.set_xlabel('seconds')
            ax.legend(('cur', 'est'), loc='lower left')
        ax.grid()
        ax.set_ylabel((self.unit if self.unit else 'it') + '/s')
        if self.unit_scale:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
            ax.yaxis.get_offset_text().set_x(-0.15)
        self.wasion = plt.isinteractive()
        plt.ion()
        self.ax = ax

    def close(self):
        if self.disable:
            return
        self.disable = True
        with self.get_lock():
            self._instances.remove(self)
        self.mpl.rcParams['toolbar'] = self.toolbar
        if not self.wasion:
            self.plt.ioff()
        if self.leave:
            self.display()
        else:
            self.plt.close(self.fig)

    def clear(self, *_, **__):
        pass

    def display(self, *_, **__):
        n = self.n
        cur_t = self._time()
        elapsed = cur_t - self.start_t
        delta_it = n - self.last_print_n
        delta_t = cur_t - self.last_print_t
        total = self.total
        xdata = self.xdata
        ydata = self.ydata
        zdata = self.zdata
        ax = self.ax
        line1 = self.line1
        line2 = self.line2
        y = delta_it / delta_t
        z = n / elapsed
        xdata.append(n * 100.0 / total if total else cur_t)
        ydata.append(y)
        zdata.append(z)
        if not total and elapsed > 66:
            xdata.popleft()
            ydata.popleft()
            zdata.popleft()
        ymin, ymax = ax.get_ylim()
        if y > ymax or z > ymax:
            ymax = 1.1 * y
            ax.set_ylim(ymin, ymax)
            ax.figure.canvas.draw()
        if total:
            line1.set_data(xdata, ydata)
            line2.set_data(xdata, zdata)
            try:
                poly_lims = self.hspan.get_xy()
            except AttributeError:
                self.hspan = self.plt.axhspan(0, 0.001, xmin=0, xmax=0, color='g')
                poly_lims = self.hspan.get_xy()
            poly_lims[0, 1] = ymin
            poly_lims[1, 1] = ymax
            poly_lims[2] = [n / total, ymax]
            poly_lims[3] = [poly_lims[2, 0], ymin]
            if len(poly_lims) > 4:
                poly_lims[4, 1] = ymin
            self.hspan.set_xy(poly_lims)
        else:
            t_ago = [cur_t - i for i in xdata]
            line1.set_data(t_ago, ydata)
            line2.set_data(t_ago, zdata)
        d = self.format_dict
        d['bar_format'] = (d['bar_format'] or '{l_bar}<bar/>{r_bar}').replace('{bar}', '<bar/>')
        msg = self.format_meter(**d)
        if '<bar/>' in msg:
            msg = ''.join(re.split('\\|?<bar/>\\|?', msg, 1))
        ax.set_title(msg, fontname='DejaVu Sans Mono', fontsize=11)
        self.plt.pause(1e-09)

def tgrange(*args, **kwargs):
    """Shortcut for `tqdm.gui.tqdm(range(*args), **kwargs)`."""
    return tqdm_gui(range(*args), **kwargs)
tqdm = tqdm_gui
trange = tgrange