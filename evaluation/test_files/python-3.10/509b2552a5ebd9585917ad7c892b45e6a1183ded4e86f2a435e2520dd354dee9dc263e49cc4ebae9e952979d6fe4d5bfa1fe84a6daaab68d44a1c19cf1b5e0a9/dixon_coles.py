import warnings
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import poisson
from .football_probability_grid import FootballProbabilityGrid
from .utils import rho_correction_vec

class DixonColesGoalModel:
    """Dixon and Coles adjusted Poisson model for predicting outcomes of football
    (soccer) matches

    Methods
    -------
    fit()
        fits a Dixon and Coles adjusted Poisson model to the data to calculate the team strengths.
        Must be called before the model can be used to predict game outcomes

    predict(home_team, away_team, max_goals=15)
        predict the outcome of a football (soccer) game between the home_team and away_team

    get_params()
        Returns the fitted parameters from the model
    """

    def __init__(self, goals_home, goals_away, teams_home, teams_away, weights=1):
        """
        Parameters
        ----------
        goals_home : list
            A list or pd.Series of goals scored by the home_team
        goals_away : list
            A list or pd.Series of goals scored by the away_team
        teams_home : list
            A list or pd.Series of team_names for the home_team
        teams_away : list
            A list or pd.Series of team_names for the away_team
        weights : list
            A list or pd.Series of weights for the data,
            the lower the weight the less the match has on the output
        """
        self.fixtures = pd.DataFrame([goals_home, goals_away, teams_home, teams_away]).T
        self.fixtures.columns = ['goals_home', 'goals_away', 'team_home', 'team_away']
        self.fixtures['goals_home'] = self.fixtures['goals_home'].astype(int)
        self.fixtures['goals_away'] = self.fixtures['goals_away'].astype(int)
        self.fixtures['weights'] = weights
        self.teams = np.sort(np.unique(np.concatenate([teams_home, teams_away])))
        self.n_teams = len(self.teams)
        self._params = np.concatenate(([1] * self.n_teams, [-1] * self.n_teams, [0.25], [-0.1]))
        self._res = None
        self.loglikelihood = None
        self.aic = None
        self.n_params = None
        self.fitted = False

    def __repr__(self):
        repr_str = ''
        repr_str += 'Module: Penaltyblog'
        repr_str += '\n'
        repr_str += '\n'
        repr_str += 'Model: Dixon and Coles'
        repr_str += '\n'
        repr_str += '\n'
        if not self.fitted:
            repr_str += 'Status: Model not fitted'
            return repr_str
        repr_str += 'Number of parameters: {0}'.format(self.n_params)
        repr_str += '\n'
        repr_str += 'Log Likelihood: {0}'.format(round(self.loglikelihood, 3))
        repr_str += '\n'
        repr_str += 'AIC: {0}'.format(round(self.aic, 3))
        repr_str += '\n'
        repr_str += '\n'
        repr_str += '{0: <20} {1:<20} {2:<20}'.format('Team', 'Attack', 'Defence')
        repr_str += '\n'
        repr_str += '-' * 60
        repr_str += '\n'
        for (idx, team) in enumerate(self.teams):
            repr_str += '{0: <20} {1:<20} {2:<20}'.format(self.teams[idx], round(self._params[idx], 3), round(self._params[idx + self.n_teams], 3))
            repr_str += '\n'
        repr_str += '-' * 60
        repr_str += '\n'
        repr_str += 'Home Advantage: {0}'.format(round(self._params[-2], 3))
        repr_str += '\n'
        repr_str += 'Rho: {0}'.format(round(self._params[-1], 3))
        repr_str += '\n'
        return repr_str

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def _fit(params, fixtures, teams):
        """
        Internal method, not to called directly by the user
        """
        n_teams = len(teams)
        params_df = pd.DataFrame(params[:n_teams], columns=['attack']).assign(defence=params[n_teams:n_teams * 2]).assign(team=teams)
        df2 = fixtures.merge(params_df, left_on='team_home', right_on='team').rename(columns={'attack': 'home_attack', 'defence': 'home_defence'}).drop('team', axis=1).merge(params_df, left_on='team_away', right_on='team').rename(columns={'attack': 'away_attack', 'defence': 'away_defence'}).assign(hfa=params[-2]).assign(rho=params[-1])
        df2['home_exp'] = np.exp(df2['hfa'] + df2['home_attack'] + df2['away_defence'])
        df2['away_exp'] = np.exp(df2['away_attack'] + df2['home_defence'])
        df2['home_llk'] = poisson.logpmf(df2['goals_home'], df2['home_exp'])
        df2['away_llk'] = poisson.logpmf(df2['goals_away'], df2['away_exp'])
        df2['dc_adj'] = rho_correction_vec(df2)
        df2['llk'] = (df2['home_llk'] + df2['away_llk'] + np.log(df2['dc_adj'])) * df2['weights']
        return -df2['llk'].sum()

    def fit(self):
        """
        Fits the model to the data and calculates the team strengths,
        home advantage and intercept. Should be called before `predict` can be used
        """
        options = {'maxiter': 100, 'disp': False}
        constraints = [{'type': 'eq', 'fun': lambda x: sum(x[:self.n_teams]) - self.n_teams}]
        bounds = [(-3, 3)] * self.n_teams
        bounds += [(-3, 3)] * self.n_teams
        bounds += [(0, 2)]
        bounds += [(-2, 2)]
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            self._res = minimize(self._fit, self._params, args=(self.fixtures, self.teams), constraints=constraints, bounds=bounds, options=options)
        self._params = self._res['x']
        self.n_params = len(self._params)
        self.loglikelihood = self._res['fun'] * -1
        self.aic = -2 * self.loglikelihood + 2 * self.n_params
        self.fitted = True

    def predict(self, home_team, away_team, max_goals=15):
        """
        Predicts the probabilities of the different possible match outcomes

        Parameters
        ----------
        home_team : str
            The name of the home_team, must have been in the data the model was fitted on

        away_team : str
            The name of the away_team, must have been in the data the model was fitted on

        max_goals : int
            The maximum number of goals to calculate the probabilities over.
            Reducing this will improve performance slightly at the expensive of acuuracy

        Returns
        -------
        FootballProbabilityGrid
            A class providing access to a range of probabilites,
            such as 1x2, asian handicaps, over unders etc
        """
        if not self.fitted:
            raise ValueError("Model's parameters have not been fit yet, please call the `fit()` function before making any predictions")
        if home_team not in self.teams:
            raise ValueError('No parameters for home team - please ensure the team was included in the training data')
        if away_team not in self.teams:
            raise ValueError('No parameters for away team - please ensure the team was included in the training data')
        home_idx = np.where(self.teams == home_team)[0][0]
        away_idx = np.where(self.teams == away_team)[0][0]
        home_attack = self._params[home_idx]
        away_attack = self._params[away_idx]
        home_defence = self._params[home_idx + self.n_teams]
        away_defence = self._params[away_idx + self.n_teams]
        home_advantage = self._params[-2]
        rho = self._params[-1]
        home_goals = np.exp(home_advantage + home_attack + away_defence)
        away_goals = np.exp(away_attack + home_defence)
        home_goals_vector = poisson(home_goals).pmf(np.arange(0, max_goals))
        away_goals_vector = poisson(away_goals).pmf(np.arange(0, max_goals))
        m = np.outer(home_goals_vector, away_goals_vector)
        m[0, 0] *= 1 - home_goals * away_goals * rho
        m[0, 1] *= 1 + home_goals * rho
        m[1, 0] *= 1 + away_goals * rho
        m[1, 1] *= 1 - rho
        probability_grid = FootballProbabilityGrid(m, home_goals, away_goals)
        return probability_grid

    def get_params(self):
        """
        Provides access to the model's fitted parameters

        Returns
        -------
        dict
            A dict containing the model's parameters
        """
        if not self.fitted:
            raise ValueError("Model's parameters have not been fit yet, please call the `fit()` function first")
        params = dict(zip(['attack_' + team for team in self.teams] + ['defence_' + team for team in self.teams] + ['home_advantage', 'rho'], self._res['x']))
        return params