import dash
from dash import testing as dcct
from pytest import fixture
import dash
from dash import dcc
from dash import html
from visual_data import region_options, regions
import visual_data
import pytest

from selenium.webdriver.chrome.webdriver import WebDriver 



@fixture(scope="function")
def app():
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
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
    ], style={'margin': '20px', 'font-family': 'Arial', 'background-color': '#000', 'border-radius': '10px'})

    return app

@pytest.fixture(scope="function")
def dash_duo(dash_args):
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")  

  
  
    web_driver = WebDriver(executable_path='C:/chrome-win64', options=options)  
    

    return dcct.DashDuo(dash.app, dash_args, web_driver)  

def test_header(dash_duo):  
    dash_app = dash_duo.app  

    header = dash_app.find_element('#header')
    assert header is not None
    assert header.text == 'Select Region'

def test_visualization(dash_duo): 
    dash_app = dash_duo.app  

    visualization = dash_app.find_element('#line-chart')
    assert visualization is not None
    assert visualization.tag_name == 'svg'

def test_region_picker(dash_duo): 
    dash_app = dash_duo.app 

    region_picker = dash_app.find_element('#radio-buttons')
    assert region_picker is not None
    assert region_picker.tag_name == 'select'

def test_region_picker_change(dash_duo):  # Remove app parameter
    dash_app = dash_duo.app 

    region_picker = dash_app.find_element('#radio-buttons')
    region_picker.click()

    new_region = region_picker.get_attribute('value')
    assert new_region != regions[0]

if __name__ == '__main__':
    pytest.main()
