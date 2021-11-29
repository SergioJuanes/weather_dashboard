# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# This Python file uses the following encoding: utf-8


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.express as px
import pandas as pd
from urllib.request import urlopen
import json
#import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import os
from dotenv import load_dotenv

#from src.components importcreate_card_forecast,  ...

import datetime

# load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")



forecast_dict = {
    'Partly cloudy': 'fas fa-cloud-sun',
    'Sunny': 'fas fa-sun',
    'Patchy rain possible': 'fas fa-cloud-sun-rain',
    'Overcast': 'fas fa-cloud',
    'Moderate rain': 'fas fa-cloud-rain',
    'Heavy rain': 'fas fa-cloud-showers-heavy',
    'Cloudy':'fas fa-cloud',
    'Light freezing rain': 'fas fa-cloud-rain'

}


with open('./data/json_municipios.json') as f:
  city_options = json.load(f)


TW = 'https://unpkg.com/tailwindcss@^2/dist/tailwind.min.css'

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

# Get url for calling to weather API
def get_weather_url(city):
    return f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&q=Spain&days=4&aqi=no&alerts=no"

#forecast for city card
def get_card(city):
    url = "http://api.weatherapi.com/v1/forecast.json?key=fb14b0934bb44ed9ad9120406212209&q=" + city + "&q=Spain&days=4&aqi=no&alerts=no"
    def get_jsonparsed_data(url):
        """
        Receive the content of ``url``, parse it as JSON and return the object.

        Parameters
        ----------
        url : str

        Returns
        -------
        dict
        """
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    dic = get_jsonparsed_data(url)
    forecast_min = dic['forecast']['forecastday'][0]['day']['mintemp_c']
    forecast_max = dic['forecast']['forecastday'][0]['day']['maxtemp_c']
    forecast_conditions = dic['forecast']['forecastday'][0]['day']['condition']['text']


    df = {'T_max': forecast_max, 'T_min': forecast_min, 'Condition': forecast_conditions}
    df = pd.DataFrame(df, index=[0])

    return df

def make_table(i, json_input):
    
    df = json_input
    col_classname = "border-collapse text-center px-4 py-2 "

    # check if the row index i
    if i%2 == 0:
        col_classname = col_classname + "bg-gray-100 "
            
    if df['UV'][i] < 3:
        uv_color = "text-green-500"
    elif df['UV'][i] < 6:
        uv_color = "text-yellow-400"
    elif df['UV'][i] < 8:
        uv_color="text-yellow-600"
    elif df['UV'][i] < 11:
        uv_color="text-red-600"
    else:
        uv_color="text-purple-800"

    chance_rain = str(round(df['Chance_Rain'][i], 0)) + '%'
    chance_snow = str(round(df['Chance_Snow'][i], 0)) + '%'
    total_precip = str(round(df['TotalPrecip'][i], 0)) + ' mm'
    t_max = str(int(round(df['T_max'][i], 0))) + '°C'
    t_min = str(int(round(df['T_min'][i], 0))) + '°C'
    wind = str(int(round(df['T_min'][i], 0))) + ' km/h'
    
    row_children = html.Tr([
                html.Td(df['Day_Name'][i], className=col_classname + " rounded-l-xl"),
                html.Td(
                    html.I(className=forecast_dict[df['Condition'][i]] + " fa-2x text-blue-500"),
                    className=col_classname
                ),
                html.Td(chance_rain, className=col_classname),
                html.Td(chance_snow, className=col_classname),
                html.Td(total_precip, className=col_classname),
                html.Td(t_max, className=col_classname+'text-red-600'),
                html.Td(t_min, className=col_classname+'text-blue-600'),
                html.Td(wind, className=col_classname),
                html.Td(df['UV'][i], className=col_classname + uv_color + " rounded-r-xl"),
            ])

    return row_children


app = dash.Dash(__name__, external_stylesheets=['style.css', FA, TW])

server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(children=[

    html.Div([
        dcc.Dropdown(
            id = "city-name",
            #options=city_options,
            placeholder = "Search",
            className="rounded-full"
        ),
    ], className="mt-2 mb-4"),


    html.Div([
        html.P('Weather Forecast')
    ], className = "text-2xl"
    ),


    html.Div(
        className="mt-4"
    ),

    html.Div([
        html.Div([
                html.Div([
                    html.Div([
                        html.P(
                            children = str(int(round(get_card("Valencia")['T_min'][0], 0))) + "/" + str(int(round(get_card("Valencia")['T_max'][0], 0))),
                            className = "font-bold text-sm text-gray-600"
                        ),
                        html.P(
                            className = forecast_dict[str(get_card("Valencia")['Condition'][0])] + " fa text-yellow-500 ml-2"
                        ),
                    ], className='ml-auto p-2 rounded-tl-xl flex bg-white opacity-80')
                ], className='rounded-xl 2xl:w-64 xl:w-48 md:w-32 sm:w-28 2xl:h-48 xl:h-32 md:h-20 sm:h-20 select-none flex items-end bg-cover bg-no-repeat', style={'background-image':'url("static/images/valencia.jpeg")'}),
                html.P(children='Valencia', className='text-center select-none')
        ]),
        html.Div([
                html.Div([
                    html.Div([
                        html.P(
                            children = str(int(round(get_card("Madrid")['T_min'][0], 0))) + "/" + str(int(round(get_card("Madrid")['T_max'][0], 0))),
                            className = "font-bold text-sm text-gray-600"
                        ),
                        html.P(
                            className = forecast_dict[str(get_card("Madrid")['Condition'][0])] + " fa text-yellow-500 ml-2"
                        ),
                    ], className='ml-auto p-2 rounded-tl-xl flex bg-white opacity-80')
                ], className='rounded-xl 2xl:w-64 xl:w-48 md:w-32 sm:w-28 2xl:h-48 xl:h-32 md:h-20 sm:h-20 select-none flex items-end bg-cover bg-no-repeat', style={'background-image':'url("static/images/madrid.jpg")'}),
                html.P(children='Madrid', className='text-center select-none')
        ]),
        html.Div([
                html.Div([
                    html.Div([
                        html.P(
                            children = str(int(round(get_card("Barcelona")['T_min'][0], 0))) + "/" + str(int(round(get_card("Barcelona")['T_max'][0], 0))),
                            className = "font-bold text-sm text-gray-600"
                        ),
                        html.P(
                            className = forecast_dict[str(get_card("Barcelona")['Condition'][0])] + " fa text-yellow-500 ml-2"
                        ),
                    ], className='ml-auto p-2 rounded-tl-xl flex bg-white opacity-80')
                ], className='rounded-xl 2xl:w-64 xl:w-48 md:w-32 sm:w-28 2xl:h-48 xl:h-32 md:h-20 sm:h-20 select-none flex items-end bg-cover bg-no-repeat', style={'background-image':'url("static/images/barcelona.jpg")'}),
                html.P(children='Barcelona', className='text-center select-none')
        ]),
        html.Div([
                html.Div([
                    html.Div([
                        html.P(
                            children = str(int(round(get_card("Sevilla")['T_min'][0], 0))) + "/" + str(int(round(get_card("Sevilla")['T_max'][0], 0))),
                            className = "font-bold text-sm text-gray-600"
                        ),
                        html.P(
                            className = forecast_dict[str(get_card("Sevilla")['Condition'][0])] + " fa text-yellow-500 ml-2"
                        ),
                    ], className='ml-auto p-2 rounded-tl-xl flex bg-white opacity-80')
                ], className='rounded-xl 2xl:w-64 xl:w-48 md:w-32 sm:w-28 2xl:h-48 xl:h-32 md:h-20 sm:h-20 select-none flex items-end bg-cover bg-no-repeat', style={'background-image':'url("static/images/sevilla.jpg")'}),
                html.P(children='Sevilla', className='text-center select-none')
        ]),
        html.Div([
                html.Div([
                    html.Div([
                        html.P(
                            children = str(int(round(get_card("a-coruna")['T_min'][0], 0))) + "/" + str(int(round(get_card("a-coruna")['T_max'][0], 0))),
                            className = "font-bold text-sm text-gray-600"
                        ),
                        html.P(
                            className = forecast_dict[str(get_card("a-coruna")['Condition'][0])] + " fa text-yellow-500 ml-2"
                        ),
                    ], className='ml-auto p-2 rounded-tl-xl flex bg-white opacity-80')
                ], className='rounded-xl 2xl:w-64 xl:w-48 md:w-32 sm:w-28 2xl:h-48 xl:h-32 md:h-20 sm:h-20 select-none flex items-end bg-cover bg-no-repeat', style={'background-image':'url("static/images/acorunya.jpg")'}),
                html.P(children='A Coruña', className='text-center select-none')
        ]),


    ], className='flex justify-evenly'),

    html.Div(
        id = 'city-name-div',
        className="mt-4 text-2xl"
    ),

    html.Div([

        html.Div([
            html.Div([
  
                html.Div(id = 'icon_day_one', className="forecast-card-icon"),
                html.Div([
                    html.P(
                        id = 'temp_day_one',
                        className = "flex justify-center font-bold text-gray-800"
                        ),
                    html.P(
                        id = 'forecast_day_one',
                        className = "text-gray-400"
                    ),
                ])
            ], className="justify-items-center flex flex-col items-center justify-center text-center h-28 select-none group rounded-xl bg-gray-100 hover:bg-gray-300")
        ], className="flex-grow mx-2"),

        html.Div([
            html.Div([
  
                html.Div(id = 'icon_day_two', className="forecast-card-icon"),
                html.Div([
                    html.P(
                        id = 'temp_day_two',
                        className = "flex justify-center font-bold text-gray-800"
                    ),
                    html.P(
                        id = 'forecast_day_two',
                        className = "text-gray-400"
                        ),
                ])
            ], className="justify-items-center flex flex-col items-center justify-center text-center h-28 select-none group rounded-xl bg-gray-100 hover:bg-gray-300")
        ], className="flex-grow mx-2"),

        html.Div([
            html.Div([
  
                html.Div(id = 'icon_day_three', className="forecast-card-icon"),
                html.Div([
                    html.P(
                        id = 'temp_day_three',
                        className = "flex justify-center font-bold text-gray-800"
                        ),
                    html.P(
                        id = 'forecast_day_three',
                        className = "text-gray-400"
                        ),
                ])
            ], className="justify-items-center flex flex-col items-center justify-center text-center h-28 select-none group rounded-xl bg-gray-100 hover:bg-gray-300")
        ], className="flex-grow mx-2 mb-10"),

    ], className='flex justify-evenly'),
    #forecast for the graph
    dcc.Store(id='df-forecast'),
    #forecast for the cards
    dcc.Store(id='df-forecast-three-days'),

    html.Div([
        html.Table(
            children = [
                html.Thead([
                    html.Tr([
                        html.Th("Day", className = "border-collapse px-4 py-2"),
                        html.Th("Condition", className = "border-collapse px-4 py-2"),
                        html.Th("Chance of rain", className = "border-collapse px-4 py-2"),
                        html.Th("Chance of snow", className = "border-collapse px-4 py-2"),
                        html.Th("Total precipitation", className = "border-collapse px-4 py-2"),
                        html.Th("Maximum temperature", className = "border-collapse px-4 py-2"),
                        html.Th("Minimum temperature", className = "border-collapse px-4 py-2"),
                        html.Th("Wind speed", className = "border-collapse px-4 py-2"),
                        html.Th("Ultraviolet index", className = "border-collapse px-4 py-2"),
                    ])
                ]), 
                html.Tbody(
                    id="table_day"
                )
            ],
            className="table-fixed w-full mt-6"
        ),
        dcc.Graph(id='indicator-graphic', className='mt-4'),
    ])

    
], className="p-4")

@app.callback(
    Output('city-name', 'options'),
    Input('city-name', 'search_value')
)
def update_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in city_options if search_value in o['label']]

@app.callback(Output('df-forecast', 'data'), Input('city-name', 'value'))
def clean_data(city):
    if city == None:
        city = 'Valencia'
    url = get_weather_url(city)

    def get_jsonparsed_data(url):
        """
        Receive the content of ``url``, parse it as JSON and return the object.

        Parameters
        ----------
        url : str

        Returns
        -------
        dict
        """
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    dic = get_jsonparsed_data(url)
    temp_c = [dic['forecast']['forecastday'][0]['hour'][i]['temp_c'] for i in range(0, 24, 1)]
    feel_temp_c = [dic['forecast']['forecastday'][0]['hour'][i]['feelslike_c'] for i in range(0, 24, 1)]
    hour = [dic['forecast']['forecastday'][0]['hour'][i]['time'] for i in range(0, 24, 1)]
    rain = [dic['forecast']['forecastday'][0]['hour'][i]['chance_of_rain'] for i in range(0, 24, 1)]
    humidity = [dic['forecast']['forecastday'][0]['hour'][i]['humidity'] for i in range(0, 24, 1)]
    pressure = [dic['forecast']['forecastday'][0]['hour'][i]['pressure_mb'] for i in range(0, 24, 1)]

    df = pd.DataFrame({'Temperature': temp_c, 'Hour': hour, 'FeelTemp': feel_temp_c, 'Rain': rain, 'Humidity': humidity, 'Pressure': pressure})

    return df.to_dict()

@app.callback(Output('df-forecast-three-days', 'data'), Input('city-name', 'value'))
def make_cards(city):
    if city == None:
        city = 'Valencia'
        
    url = get_weather_url(city)

    def get_jsonparsed_data(url):
        """
        Receive the content of ``url``, parse it as JSON and return the object.

        Parameters
        ----------
        url : str

        Returns
        -------
        dict
        """
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

    dic = get_jsonparsed_data(url)
    date = [dic['forecast']['forecastday'][i]['date'] for i in range(0, 3, 1)]
    forecast_min = [dic['forecast']['forecastday'][i]['day']['mintemp_c'] for i in range(0, 3, 1)]
    forecast_max = [dic['forecast']['forecastday'][i]['day']['maxtemp_c'] for i in range(0, 3, 1)]
    forecast_conditions = [dic['forecast']['forecastday'][i]['day']['condition']['text'] for i in range(0, 3, 1)]
    forecast_precip = [dic['forecast']['forecastday'][i]['day']['totalprecip_mm'] for i in range(0, 3, 1)]
    forecast_rain = [dic['forecast']['forecastday'][i]['day']['daily_chance_of_rain'] for i in range(0, 3, 1)]
    forecast_snow = [dic['forecast']['forecastday'][i]['day']['daily_chance_of_snow'] for i in range(0, 3, 1)]
    forecast_wind = [dic['forecast']['forecastday'][i]['day']['maxwind_kph'] for i in range(0, 3, 1)]
    forecast_uv = [dic['forecast']['forecastday'][i]['day']['uv'] for i in range(0, 3, 1)]

    df = pd.DataFrame({'Day': date, 'T_max': forecast_max, 'T_min': forecast_min, 'Condition': forecast_conditions, 'TotalPrecip': forecast_precip, 'Chance_Rain': forecast_rain, 'Chance_Snow': forecast_snow, 'Wind': forecast_wind, 'UV': forecast_uv})

    list_day = []
    for i in range(0, 3, 1):
        year, month, day = (int(x) for x in df['Day'][i].split('-'))    
        ans = datetime.date(year, month, day)
        list_day.append(str(day) + ', ' + ans.strftime('%A'))

    df['Day_Name'] = list_day

    return df.to_dict()


#forecast for 3 days for the selected city
@app.callback(Output('temp_day_one', 'children'), Input('df-forecast-three-days', 'data'))
def temp_day_one(json):
    df = pd.DataFrame.from_dict(data=json)
    text = html.Span(str(int(round(df['T_min'][0], 0)))), html.Span('/', className="mx-1 text-gray-500 text-sm"), html.Span(str(int(round(df['T_max'][0], 0))))
    return text

@app.callback(Output('temp_day_two', 'children'), Input('df-forecast-three-days', 'data'))
def temp_day_two(json):
    df = pd.DataFrame.from_dict(data=json)
    text = html.Span(str(int(round(df['T_min'][1], 0)))), html.Span('/', className="mx-1 text-gray-500 text-sm"), html.Span(str(int(round(df['T_max'][1], 0))))
    return text

@app.callback(Output('temp_day_three', 'children'), Input('df-forecast-three-days', 'data'))
def temp_day_three(json):
    df = pd.DataFrame.from_dict(data=json)
    text = html.Span(str(int(round(df['T_min'][2], 0)))), html.Span('/', className="mx-1 text-gray-500 text-sm"), html.Span(str(int(round(df['T_max'][2], 0))))
    return text

#day of the forecast (Nº of the day, name of the day)
@app.callback(Output('forecast_day_one', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_one(json):
    df = pd.DataFrame.from_dict(data=json)
    return df['Day_Name'][0]

@app.callback(Output('forecast_day_two', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_two(json):
    df = pd.DataFrame.from_dict(data=json)
    return df['Day_Name'][1]

@app.callback(Output('forecast_day_three', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_three(json):
    df = pd.DataFrame.from_dict(data=json)
    return df['Day_Name'][2]

#icon of the forecast
@app.callback(Output('icon_day_one', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_one(json):
    df = pd.DataFrame.from_dict(data=json)
    return html.I(className=forecast_dict[df['Condition'][0]] + " fa-2x text-blue-500")

@app.callback(Output('icon_day_two', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_two(json):
    df = pd.DataFrame.from_dict(data=json)
    return html.I(className=forecast_dict[df['Condition'][1]] + " fa-2x text-blue-500")

@app.callback(Output('icon_day_three', 'children'), Input('df-forecast-three-days', 'data'))
def forec_day_three(json):
    df = pd.DataFrame.from_dict(data=json)
    return html.I(className=forecast_dict[df['Condition'][2]] + " fa-2x text-blue-500")

@app.callback(Output('table_day', 'children'), Input('df-forecast-three-days', 'data'))
def make_table_forecast(json):
    df = pd.DataFrame.from_dict(data=json)
    row_tbl = [make_table(i, df) for i in range(0, len(df))]
    return row_tbl


@app.callback(
    Output('city-name-div', 'children'),
    Input('city-name', 'value')
)
def get_city_name(city):
    if city == None:
        city = 'Valencia'
    return list(filter(lambda city_options: city_options['value'] == city, city_options))[0]['label']

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('df-forecast', 'data'),
    Input('city-name', 'value')
)
#print the graph of daily evolution of forecast when you call a city
def graph(json, city):
    if city == None:
        city = 'Valencia'

    df = pd.DataFrame.from_dict(data=json)
    
    template = "plotly_white+xgridoff"

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces


    fig.add_trace(
        go.Scatter(x=df['Hour'], y=df['Humidity'], name='Humidity', hovertemplate='%{y}%', line=dict(color='#04DACD')),
        secondary_y=True,
    )

    fig.add_trace(
        go.Scatter(x=df['Hour'], y=df['FeelTemp'], name='Feel like', hovertemplate='%{y}°C', line=dict(color='#DA7C04')),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df['Hour'], y=df['Temperature'], name='Temperature', hovertemplate='%{y}°C', line=dict(color='#DA2404')),
        secondary_y=False,
    )



    fig.add_trace(
        go.Scatter(x=df['Hour'], y=df['Rain'], name='Probability of rain', hovertemplate='%{y}%', line=dict(color='#0489DA')),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        template=template
    )
    fig.update_traces(mode='lines+markers')


    # Set x-axes and y-axes
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(title_text="Temperature", color='#DA2404', secondary_y=False, showline=True, linewidth=1, linecolor='black', mirror=True)
    fig.update_yaxes(title_text="Humidity", color='#04DACD', secondary_y=True, showline=True, linewidth=1, linecolor='black', mirror=True, range =[0, 100])

    # Personalize hover (tooltip) info
    fig.update_layout(hovermode="x unified", hoverdistance=200)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="#f2f2f2",
            font_size=14,
        )
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ))
    fig.update_layout(
        title= {
            'text':"Forecast in " + list(filter(lambda city_options: city_options['value'] == city, city_options))[0]['label'],
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            }
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)