import pandas as pd
import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
from beartype import beartype
import random
from typing import Optional

@beartype
def _plot_net_benefit(plot_df: pd.DataFrame, y_limits: list=[-0.05, 0.2], color_names: Optional[list]=None) -> None:
    modelnames = plot_df['model'].value_counts().index
    if color_names is None:
        get_colors = lambda n: ['#%06x' % random.randint(0, 16777215) for _ in range(n)]
        color_names = get_colors(len(modelnames))
    for (modelname, color_name) in zip(modelnames, color_names):
        single_model_df = plot_df[plot_df['model'] == modelname]
        x_vals = single_model_df['threshold']
        y_vals = single_model_df['net_benefit']
        plt.plot(x_vals, y_vals, color=color_name)
        plt.ylim(y_limits)
        plt.legend(modelnames)
        plt.grid(b=True, which='both', axis='both')
        plt.xlabel('Threshold Values')
        plt.ylabel('Calculated Net Benefit')
    plt.show()

@beartype
def _plot_net_intervention_avoided(plot_df: pd.DataFrame, y_limits: list=[-0.05, 0.2], color_names: Optional[list]=None) -> None:
    modelnames = plot_df['model'].value_counts().index
    if color_names is None:
        get_colors = lambda n: ['#%06x' % random.randint(0, 16777215) for _ in range(n)]
        color_names = get_colors(len(modelnames))
    for (modelname, color_name) in zip(modelnames, color_names):
        single_model_df = plot_df[plot_df['model'] == modelname]
        plt.plot(single_model_df['threshold'], single_model_df['net_intervention_avoided'], color=color_name)
        plt.ylim(y_limits)
        plt.legend(modelnames)
        plt.grid(b=True, which='both', axis='both')
        plt.xlabel('Threshold Values')
        plt.ylabel('Calculated Net Reduction of Interventions Per 100 Patients')
    plt.show()

@beartype
def plot_graphs(plot_df: pd.DataFrame, graph_type: str='net_benefit', y_limits: list=[-0.05, 1], color_names: list=['blue', 'purple', 'red', 'green', 'hotpink', 'orange', 'saddlebrown', 'lime', 'magenta']) -> None:
    if graph_type not in ['net_benefit', 'net_intervention_avoided']:
        ValueError('graph_type must be one of 2 strings: net_benefit, net_intervention_avoided')
    if graph_type == 'net_intervention_avoided':
        if 'net_intervention_avoided' not in plot_df.columns:
            ValueError('You must calculate net interventions avoided and include it in the input dataframe to plot')
    if graph_type == 'net_benefit':
        _plot_net_benefit(plot_df=plot_df, y_limits=y_limits, color_names=color_names)
    elif graph_type == 'net_intervention_avoided':
        _plot_net_intervention_avoided(plot_df=plot_df, y_limits=y_limits, color_names=color_names)
    return