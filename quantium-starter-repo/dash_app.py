import dash
from dash import dcc, html
import pandas as pd

dtfl = pd.read_csv('managed_data.csv')

dtfl['date'] = pd.to_datetime(dtfl['date'])


app = dash.Dash(__name__)

bar_chart = dcc.Graph(
    id='line-chart',
    figure={
        'data': [
            {'x': dtfl['date'], 'y': dtfl['sales'], 'type': 'line', 'name': 'Sales'},
        ],
        'layout': {
            'title': 'Analysing Pink Morsel Data',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Sales'},
            
        }
    }
)

app.layout = html.Div([
    bar_chart
])

if __name__ == '__main__':
    app.run_server(debug=True)
