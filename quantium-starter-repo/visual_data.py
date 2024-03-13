import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

dtfl = pd.read_csv('formatted_data.csv')

dtfl['date'] = pd.to_datetime(dtfl['date'])

app = dash.Dash(__name__)

regions = dtfl['region'].unique()
region_options = [{'label': region, 'value': region} for region in regions]
region_options.append({'label': 'all', 'value': 'All'})

app.layout = html.Div([
    html.Div([
        html.H1('Select Region', style={'textAlign': 'center', 'color': '#fff', 'font-family': 'Arial', 'margin-bottom': '20px'}),
        dcc.RadioItems(
            id='radio-buttons',
            options=region_options,
            value=regions[0], 
            labelStyle={'display': 'inline-block', 'font-family': 'Arial', 'font-size': '16px', 'margin': '10px', 'cursor': 'pointer', 'color': 'grey'},
        ),
        html.P(id='comparison-results', style={'color': '#ddd', 'font-family': 'Arial', 'fontSize': '18px', 'textAlign': 'center', 'margin-top': '20px'}),
    ],style={'padding': '20px', 'border': '1px solid #333', 'border-radius': '5px', 'background-color': '#222'}),
    html.Div([
        dcc.Graph(id='line-chart'),
    ]),
], style={'margin': '20px', 'font-family': 'Arial', 'background-color': '#000', 'border-radius': '10px'})

@app.callback(
    [Output('line-chart', 'figure'),
     Output('comparison-results', 'children')],
    [Input('radio-buttons', 'value')]
)




def update_chart(sltd_rgn):
    if sltd_rgn == 'All':
        filtered_dtfl = dtfl 
        sltd_rgn_label = 'All Regions'
    else:
        filtered_dtfl = dtfl[dtfl['region'] == sltd_rgn]
        sltd_rgn_label = sltd_rgn

    figure = {
        'data': [
            {'x': filtered_dtfl['date'], 'y': filtered_dtfl['sales'], 'type': 'line', 'name': 'Sales'},
        ],
        'layout': {
            'title': f'Sales in {sltd_rgn_label}',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Sales'},
        }
    }

    sales_after_jan_15 = filtered_dtfl[filtered_dtfl['date'] > '2021-01-15']
    sales_increased = sales_after_jan_15['sales'].diff().gt(0).any()

    if sales_increased:
        cmprn_rslt = "Sales showed improvement after January 15, 2021"
    else:
        cmprn_rslt = "Sales declined after January 15, 2021."


    return figure, cmprn_rslt

if __name__ == '__main__':
    app.run_server(debug=True)