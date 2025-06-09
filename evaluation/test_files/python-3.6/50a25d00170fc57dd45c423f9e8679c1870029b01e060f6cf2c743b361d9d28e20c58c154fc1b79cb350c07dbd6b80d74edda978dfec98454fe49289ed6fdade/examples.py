import numpy as np
import pandas as pd
TARGETS = {'binary': lambda x: np.random.choice([0, 1], size=x), 'continuous': lambda x: np.random.normal(0, 1, x)}

def generate_random_data(clusters, dates, N, target='continuous'):
    users = [f'User {i}' for i in range(1000)]
    target_values = TARGETS[target](N)
    df = pd.DataFrame({'cluster': np.random.choice(clusters, size=N), 'target': target_values, 'user': np.random.choice(users, size=N), 'date': np.random.choice(dates, size=N)})
    return df

def generate_non_clustered_data(N, n_users):
    users = [f'User {i}' for i in range(n_users)]
    df = pd.DataFrame({'target': np.random.normal(0, 1, size=N), 'user': np.random.choice(users, size=N)})
    return df
binary_df = pd.DataFrame({'target': [0, 1, 0, 1], 'treatment': ['A', 'B', 'B', 'A']})
continuous_df = pd.DataFrame({'target': [0.5, 0.5, 0.5, 0.5], 'treatment': ['A', 'B', 'B', 'A']})
analysis_df = pd.DataFrame({'target': [0, 1, 0, 1], 'treatment': ['A', 'B', 'B', 'A'], 'cluster': ['Cluster 1', 'Cluster 1', 'Cluster 1', 'Cluster 1'], 'date': ['2022-01-01', '2022-01-01', '2022-01-01', '2022-01-01']})

def generate_clustered_data():
    analysis_df = pd.DataFrame({'country_code': ['ES'] * 4 + ['IT'] * 4 + ['PL'] * 4 + ['RO'] * 4, 'city_code': ['BCN', 'BCN', 'MAD', 'BCN'] + ['NAP'] * 4 + ['WAW'] * 4 + ['BUC'] * 4, 'user_id': [1, 1, 2, 1, 3, 4, 5, 6, 7, 8, 8, 8, 9, 9, 9, 10], 'date': ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04'] * 4, 'treatment': ['A', 'A', 'B', 'A', 'B', 'B', 'A', 'B', 'B', 'A', 'A', 'A', 'B', 'B', 'B', 'A'], 'target': [0.01] * 15 + [0.1]})
    return analysis_df