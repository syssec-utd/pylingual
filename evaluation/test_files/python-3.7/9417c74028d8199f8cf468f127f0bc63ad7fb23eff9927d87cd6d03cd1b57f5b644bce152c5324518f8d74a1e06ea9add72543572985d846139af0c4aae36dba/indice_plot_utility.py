from plotly.subplots import make_subplots
import plotly.graph_objs as go

def generate_rebalanced_indice_weight_composition(weights_df=None):
    if weights_df is None:
        fig = make_subplots(rows=2, cols=1)
        fig.update_layout(height=600, width=1600, title_text='computations cannot be completed')
        return fig
    else:
        fig = make_subplots(rows=2, cols=1)
        fig.append_trace(go.Scatter(x=weights_df.index, y=weights_df.indice, name='Rebalanced Indice', opacity=0.8), row=1, col=1)
        constituents = [col for col in weights_df.columns if col not in ['indice']]
        for me_constituent in constituents:
            trace_sig = go.Scatter(x=weights_df.index, y=weights_df[me_constituent], name=me_constituent, opacity=0.8)
            fig.append_trace(trace_sig, row=2, col=1)
        fig.update_layout(height=600, width=1600, title_text='Weights composition', showlegend=True)
        return fig

def generate_rebalanced_indice(weights_df=None, title='Rebalanced Indice Value', error_message=None):
    if weights_df is None:
        fig = make_subplots(rows=2, cols=1)
        if error_message is not None:
            fig.update_layout(height=600, width=1600, title_text=error_message)
        else:
            fig.update_layout(height=600, width=1600, title_text='computations cannot be completed')
        return fig
    else:
        fig = make_subplots(rows=1, cols=1)
        fig.append_trace(go.Scatter(x=weights_df.index, y=weights_df.indice, name='Rebalanced Indice', opacity=0.8), row=1, col=1)
        fig.update_layout(height=600, width=1600, title_text=title, showlegend=True)
        fig.update_xaxes(rangeslider_visible=True)
        return fig

def generate_weight_composition(weights_df=None, error_message=None):
    if weights_df is None:
        fig = make_subplots(rows=1, cols=1)
        if error_message is not None:
            fig.update_layout(height=600, width=1600, title_text=error_message)
        else:
            fig.update_layout(height=600, width=1600, title_text='computations cannot be completed')
        return fig
    else:
        if 'is_rebalancing' in list(weights_df.columns):
            weights_df = weights_df.drop(columns=['is_rebalancing'])
        fig = make_subplots(rows=1, cols=1)
        constituents = [col for col in weights_df.columns if col not in ['indice']]
        for me_constituent in constituents:
            trace_sig = go.Scatter(x=weights_df.index, y=weights_df[me_constituent], name=me_constituent, opacity=0.8)
            fig.append_trace(trace_sig, row=1, col=1)
        fig.update_layout(height=600, width=1600, title_text='Weights Composition', showlegend=True)
        fig.update_xaxes(rangeslider_visible=True)
        return fig

def generate_simple_timeseries_plot(data=None, title=''):
    fig = make_subplots(rows=1, cols=1)
    for me_constituent in data.columns:
        trace_sig = go.Scatter(x=data.index, y=data[me_constituent], name=me_constituent, opacity=0.8)
        fig.append_trace(trace_sig, row=1, col=1)
    fig.update_layout(height=600, width=1600, title_text=title, showlegend=True)
    fig.update_xaxes(rangeslider_visible=True)
    return fig