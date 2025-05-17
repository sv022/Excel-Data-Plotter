import pandas as pd
import plotly.graph_objects as go
from ipywidgets import interact, Dropdown

def plot_3d_scatter(csv_file, view='points'):
    # Чтение данных из CSV
    df = pd.read_excel(csv_file)
    
    # Получение списка числовых столбцов
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) < 3:
        print("Для построения 3D-графика нужно как минимум 3 числовых столбца!")
        return
    
    # Функция для интерактивного выбора переменных
    @interact
    def interactive_3d_plot(
        x_axis=Dropdown(options=numeric_cols, value=numeric_cols[0], description='Ось X:'),
        y_axis=Dropdown(options=numeric_cols, value=numeric_cols[1], description='Ось Y:'),
        z_axis=Dropdown(options=numeric_cols, value=numeric_cols[4], description='Ось Z:'),
        color_by=Dropdown(options=numeric_cols+[None], value=None, description='Цвет по:'),
        marker_size=5
    ):
        # Создание 3D-графика
        fig = go.Figure()
        
        # Добавление точек
        if view == 'points':
            fig.add_trace(go.Scatter3d(
                x=df[x_axis],
                y=df[y_axis],
                z=df[z_axis],
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=df[color_by] if color_by else None,
                    colorscale='Viridis',
                    opacity=0.8,
                    colorbar=dict(title=color_by) if color_by else None
                ),
                name='Точки данных'
            ))
        else:
            fig.add_trace(go.Surface(z=df.pivot_table(values=z_axis, index=x_axis, columns=y_axis).values))
        
        # Настройка макета
        
        fig.update_layout(
            title=f'3D график: {z_axis} = f({x_axis}, {y_axis})',
            scene=dict(
                xaxis_title=x_axis,
                yaxis_title=y_axis,
                zaxis_title=z_axis, 
            ),
            width=1920,
            height=1080,
            margin=dict(l=0, r=0, b=0, t=30)
        )
        
        fig.show()

    return interactive_3d_plot

# Использование функции
plotter = plot_3d_scatter('results.xlsx')  # Укажите путь к вашему CSV-файлу