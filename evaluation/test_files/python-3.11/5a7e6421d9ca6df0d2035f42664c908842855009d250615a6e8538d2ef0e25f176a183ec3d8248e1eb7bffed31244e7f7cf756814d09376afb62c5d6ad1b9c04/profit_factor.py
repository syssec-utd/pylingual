from typing import Any, Optional
import numpy as np
import pandas as pd
from nautilus_trader.analysis.statistic import PortfolioStatistic

class ProfitFactor(PortfolioStatistic):
    """
    Calculates the annualized profit factor or ratio (wins/loss).
    """

    def calculate_from_returns(self, returns: pd.Series) -> Optional[Any]:
        if not self._check_valid_returns(returns):
            return np.nan
        return abs(returns[returns >= 0].sum() / returns[returns < 0].sum())