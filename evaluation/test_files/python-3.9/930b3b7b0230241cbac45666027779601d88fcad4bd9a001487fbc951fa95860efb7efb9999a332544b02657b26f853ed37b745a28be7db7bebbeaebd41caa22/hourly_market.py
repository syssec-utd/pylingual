""" Object to analyze the market. """
from cryptotoolbox.utility import metrics
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
from matplotlib import pyplot as plt
from cryptotoolbox.tools.time_tools import _parse_date, parser_date
from cryptotoolbox.tools.analyze_tools import roll_corr
__all__ = ['MarketAnalyzer']

class MarketAnalyzer:
    """ Analyze and compare each other asset indices.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe of market data.
    base : float, optional
        Base to compare asset performances, default is 100.

    Methods
    -------
    set_index
    _set_assets
    _set_metric
    get_perf
    get_corr
    get_kpi

    Attributes
    ----------
    df, portfolio : pd.DataFrame
        Observations on which the metrics are computed, analyzed and compared.
    idx : array-like
        Period over which the metrics are computed, analyzed and compared.
    assets : list of str
        Assets on which the metrics are computed, analyzed and compared.
    metrics : list of str
        List of metrics to compute.

    """
    df = pd.DataFrame()
    portfolio = pd.DataFrame()
    idx = []
    assets = []
    n = 0
    parser_metrics = {'sharpe': {'f': metrics.sharpe, 'p': {'period': 252 * 24}}, 'calmar': {'f': metrics.calmar, 'p': {'period': 252 * 24}}, 'annual_return': {'f': metrics.annual_return, 'p': {'period': 252 * 24}}, 'annual_volatility': {'f': metrics.annual_volatility, 'p': {'period': 252 * 24}}, 'mdd': {'f': metrics.mdd, 'p': {}}}
    metrics = []
    m = 0
    green_red = sns.diverging_palette(17, 170, n=5, l=70, as_cmap=True)
    red_green = sns.diverging_palette(170, 17, n=5, l=70, as_cmap=True)

    def __init__(self, data, base=100.0):
        """ Initialize object. """
        self.base = base
        self.DF = data
        (self.T, self.N) = data.shape
        self.IDX = data.index
        self._set_index(min(self.IDX), max(self.IDX))
        self._set_assets(list(data.columns))
        self.set_metric('annual_return', 'annual_volatility', 'sharpe', 'calmar', 'mdd')

    def _set_hours_per_year(self):
        self.n_hours_per_year = 252 * 24
        for m in self.parser_metrics.keys():
            if 'period' in self.parser_metrics[m]['p'].keys():
                self.parser_metrics[m]['p']['period'] = self.n_hours_per_year

    def get_index(self, start, end=None):
        """ Get selected index from `start` to `end` period.
        Parameters
        ----------
        start : str, int or datetime.date
            - Select the first period with int, datetime.date or str with
                format 'YYYY-MM-DD'.
            - Select a period until to `end` with str as {'ytd', 'qtd', 'mtd',
                'y', 'q', 'm', 'w', 'd'} and you can append an int before the
                period, e.g '3y', '8w', etc.
        end : str, int or datetime.date
            Last period to select, must be match with format of dataframe
            index. Default is the last period available.

        Returns
        -------
        pd.Index
            The selected index period.

        """
        if end is None:
            end = self.IDX[-1]
        end = _parse_date(end, self.IDX)
        if isinstance(start, str) and '-' not in start:
            start = parser_date(end, period=start)
        start = _parse_date(start, self.IDX)
        if start >= end:
            raise ValueError('{} is greater or equal than {}.'.format(start, end))
        return self.IDX[(self.IDX >= start) & (self.IDX <= end)]

    def _set_data(self, idx, assets):
        """ Set dataframe on which metrics are computed and analyzed. """
        if self.n >= self.N:
            assets = slice(None)
        if idx.size >= self.IDX.size:
            idx = slice(None)
        self.df = self.DF.loc[idx, assets].dropna(axis=1, how='all').dropna(axis=0, how='any').copy()
        self.idx = self.df.index

    def set_perimeter(self, assets, start, end=None):
        self._set_assets(assets)
        self._set_index(start, end)

    def _set_index(self, start, end=None):
        """ Select starting and ending period to analyze.
        Parameters
        ----------
        start : str, int or datetime.date
            - Select the first period with int, datetime.date or str with
                format 'YYYY-MM-DD'.
            - Select a period until to `end` with str as {'ytd', 'qtd', 'mtd',
                'y', 'q', 'm', 'w', 'd'} and you can append an int before the
                period, e.g '3y', '8w', etc.
        end : str, int or datetime.date
            Last period to select, must be match with format of dataframe
            index. Default is the last period available.

        """
        try:
            idx = self.get_index(start, end)
        except ValueError:
            pass
        else:
            self._set_data(idx, self.assets)
            self._set_hours_per_year()

    def _set_assets(self, assets):
        """ Set assets to analyze and compare.
        Parameters
        ----------
        assets : list of str
            Name of assets to select in `DF`.

        """
        self.assets = assets
        self.n = len(assets)
        self._set_data(self.idx, self.assets)

    def set_metric(self, *metrics):
        """ Set metrics to compute.

        Parameters
        ----------
        *metrics : {'annual_return', 'annual_volatility', 'calmar', 'mdd',                 'sharpe', 'z_score'}
            Name of metrics to compute.

        """
        self.metrics = metrics
        self.m = len(metrics)

    def get_kpi(self, drop_duplicate=True):
        """ Compute some key performance indicators and set them in a table.

        Returns
        -------
        pd.DataFrame
            Table of key performance indicators.

        """
        results = np.zeros([self.m, self.n])
        i = 0
        for m in self.metrics:
            j = 0
            (f, p) = (self.parser_metrics[m][k] for k in ['f', 'p'])
            if 'lags' in p.keys():
                p['lags'] = min(63, max(self.df.shape[0] - 1, 1))
            for a in self.assets:
                results[i, j] = f(getattr(self.df, a).values, **p)
                j += 1
            i += 1
        kpis_df = pd.DataFrame(results, columns=self.assets, index=self.metrics)
        if drop_duplicate:
            print('dropping duplicate')
            kpis_df = kpis_df.T.drop_duplicates().T
        return kpis_df

    def display_kpi(self, title='KPI table'):
        """ Display KPI. """
        df = self.get_kpi().T
        df.index.name = title
        if 'mdd' in self.metrics:
            df.mdd = -df.mdd
        style = df.style.background_gradient(cmap=self.green_red, subset=[a for a in self.metrics if a != 'annual_volatility']).background_gradient(cmap=self.red_green, subset=[a for a in self.metrics if a == 'annual_volatility']).format({'annual_return': '{:.2%}', 'annual_volatility': '{:.2%}', 'sharpe': '{:.2f}', 'calmar': '{:.2f}', 'mdd': '{:.2%}', 'z_score': '{:.2f}'})
        display(style)

    def get_perf(self):
        """ Get asset performances.

        Returns
        -------
        pd.DataFrame
            Performance of assets.

        """
        return self.base * self.df / self.df.iloc[0, :].values

    def plot_perf(self, title='Performances', saving_png_path=None, ax=None, show=True, **kwargs):
        """ Plot asset performances.

        Parameters
        ----------
        title : str, optional
            Title to display on the graph, default is 'Performances'.
        ax : matplotlib.Axes, optional
            Axes object to plot the performances. Default is None it will
            create a new one ax object.
        show : bool, optional
            If true display the figure. May useful to update already existing
            ax object. Default is True.
        **kwargs
            Keyword arguments passed to ``plot`` method.

        """
        df = self.get_perf()
        if ax is None:
            (f, ax) = plt.subplots(1, 1, figsize=(16, 16))
        if not df.empty:
            df.plot(ax=ax, title=title, **kwargs)
        if saving_png_path is not None:
            plt.savefig(saving_png_path, format='png')
        if show:
            plt.show()

    def get_corr(self, window):
        """ Get rolling cross-correlation.

        Returns
        -------
        pd.DataFrame
            Rolling pairwise correlation of assets.

        """
        if self.n < 2:
            return pd.DataFrame()
        if isinstance(window, str):
            w = int(window[:-1])
        else:
            w = int(window)
        i = self.IDX[max(np.argmax(self.IDX == self.idx[0]) - w, 0)]
        idx = self.get_index(i, self.idx[-1])
        df = self.DF.loc[idx, self.assets]
        return roll_corr(df, window=window).loc[self.idx, :].dropna()

    def get_stacked_corr(self, window):
        """ Get rolling cross-correlation.
        Returns
        -------
        pd.DataFrame
            Rolling pairwise correlation of assets.
        """
        if self.n < 2:
            return pd.DataFrame()
        if isinstance(window, str):
            w = int(window[:-1])
        else:
            w = int(window)
        i = self.IDX[max(np.argmax(self.IDX == self.idx[0]) - w, 0)]
        idx = self.get_index(i, self.idx[-1])
        df = self.DF.loc[idx, self.assets]
        mat_roll_cor = df.rolling(window).corr()
        return mat_roll_cor