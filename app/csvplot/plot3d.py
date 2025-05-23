import pandas as pd
import plotly.graph_objects as go


def plot3d(df, screen_size, view='points'):    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 3:
        return
    
    def interactive_3d_plot(
        x_axis=numeric_cols[1],
        y_axis=numeric_cols[2],
        z_axis=numeric_cols[0],
        marker_size=5
    ):
        fig = go.Figure()
        
        if view == 'points':
            fig.add_trace(go.Scatter3d(
                x=df[x_axis],
                y=df[y_axis],
                z=df[z_axis],
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=None,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=None
                ),
                name='Точки данных'
            ))
        else:
            fig.add_trace(go.Surface(z=df.pivot_table(values=z_axis, index=x_axis, columns=y_axis).values))
            
        fig.update_layout(
            title=f'3D график: {z_axis} = f({x_axis}, {y_axis})',
            scene=dict(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                zaxis_title=z_axis, 
            ),
            width=screen_size[0],
            height=screen_size[1],
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        fig.show()

    return interactive_3d_plot()
