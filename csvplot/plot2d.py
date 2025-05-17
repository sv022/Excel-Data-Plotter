from math import log2
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Чтение CSV-файла
df = pd.read_excel('example2d.xlsx')  # Укажите путь к вашему файлу

independent_var = df.columns[0]  # Можно изменить на нужный столбец, например 'x'

# Создание субплотов
dependent_vars = [col for col in df.columns if col != independent_var]
num_plots = len(dependent_vars)
num_cols = int(log2(num_plots))
fig = make_subplots(rows=num_plots, cols=num_cols, 
                    subplot_titles=[f"{independent_var} → {var}" for var in dependent_vars])


# Добавление графиков для каждой зависимой переменной
for i, var in enumerate(dependent_vars):
    fig.add_trace(
        go.Scatter(x=df[independent_var], y=df[var], name=var),
        row=i//num_cols+1, col=i%num_cols+1
    )
    
    # Настройка осей для каждого субплота
    fig.update_xaxes(title_text=independent_var, row=i, col=1)
    fig.update_yaxes(title_text=var, row=i, col=1)

# Общие настройки
fig.update_layout(
    autosize=False,
    width=num_cols*400,
    height=500*num_plots,  # Высота зависит от количества графиков
    title_text=f"Графики зависимостей от {independent_var}",
    showlegend=False,
)

# Показать график
fig.show()