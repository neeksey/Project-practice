import dash
from dash import dcc, html, dash_table  # Добавлен импорт dash_table
from dash.dependencies import Input, Output
import pandas as pd
import requests
import plotly.express as px

# Инициализируем приложение
app = dash.Dash(__name__)

# Функция для получения данных из API
def fetch_data():
    try:
        response = requests.get('http://localhost:8000/grades/')  # Замените на ваш URL API
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных: {e}")
        return []  # Возвращаем пустой список в случае ошибки

# Преобразуем JSON данные в DataFrame
def create_dataframe(data):
    records = []
    for entry in data:
        records.append({
            "Студент": f"{entry['student']['first_name']} {entry['student']['last_name']}",
            "Предмет": entry['subject']['name'],
            "Учитель": f"{entry['teacher']['first_name']} {entry['teacher']['last_name']}",
            "Оценка": entry['score'],
            "Дата": entry['date_recorded']
        })
    return pd.DataFrame(records)

# Определяем макет приложения
app.layout = html.Div(children=[
    html.H1(children='Успеваемость студентов'),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # Обновление каждые 10 секунд
        n_intervals=0  # Начальное значение
    ),
    dash_table.DataTable(  # Используем dash_table.DataTable
        id='grades-table',
        page_size=10,
        columns=[],
        data=[]
    ),
    dcc.Graph(id='grades-graph'),  # График для отображения данных
    html.Div(id='error-message', style={'color': 'red'})  # Для отображения ошибок
])

# Callback для обновления таблицы и графика
@app.callback(
    [
        Output('grades-table', 'data'),
        Output('grades-table', 'columns'),
        Output('grades-graph', 'figure'),  # Возвращаем данные графика
        Output('error-message', 'children')
    ],
    [Input('interval-component', 'n_intervals')]
)
def update_content(n):
    data = fetch_data()  # Получаем данные из API
    if not data:
        return [], [], {}, "Не удалось загрузить данные."  # Возвращаем сообщение об ошибке

    df = create_dataframe(data)  # Создаем DataFrame из данных

    # Обновление таблицы
    columns = [{"name": col, "id": col} for col in df.columns]
    table_data = df.to_dict('records')

    # Создание отдельных круговых диаграмм по каждому предмету
    subjects = df['Предмет'].unique()  # Получаем список уникальных предметов
    fig = None

    if len(subjects) > 0:
        fig = px.pie(
            df,
            names='Оценка',  # Оценки будут сегментами
            facet_col='Предмет',  # Разделяем диаграммы по предметам
            title='Распределение оценок по предметам',
            labels={'Оценка': 'Оценка'}
        )

        # Настройка внешнего вида диаграммы
        fig.update_layout(
            title_x=0.5,  # Центрирование заголовка
            template='plotly'  # Улучшение визуального стиля
        )

    return table_data, columns, fig, ""  # Возвращаем данные таблицы, столбцы, график и пустое сообщение об ошибке

# Запускаем приложение
if __name__ == '__main__':
    app.run(debug=True)