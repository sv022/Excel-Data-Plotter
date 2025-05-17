from math import log2
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot2d(df):
    independent_var = df.columns[0]

    dependent_vars = [col for col in df.columns if col != independent_var]
    num_plots = len(dependent_vars)
    num_cols = int(log2(num_plots)) if num_plots > 1 else 1
    fig = make_subplots(rows=num_plots, cols=num_cols, 
                        subplot_titles=[f"{var} → {independent_var}" for var in dependent_vars])


    for i, var in enumerate(dependent_vars):
        fig.add_trace(
            go.Scatter(x=df[var], y=df[independent_var], name=var, mode="markers"),
            row=i//num_cols+1, col=i%num_cols+1
        )
        
        fig.update_xaxes(title_text=var, row=i//num_cols+1, col=i%num_cols+1)
        fig.update_yaxes(title_text=independent_var, row=i//num_cols+1, col=i%num_cols+1)

    # Общие настройки
    fig.update_layout(
        autosize=False,
        width=num_cols*400,
        height=500*num_plots,
        title_text=f"Графики зависимостей от {independent_var}",
        showlegend=False,
    )

    fig.show()