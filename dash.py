#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
from dash import dcc
import dash_core_components as dcc
from dash import html
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
import requests
import pandas as pd
from datetime import date
import numpy as np
import dash_bootstrap_components as dbc
import os


# In[11]:


app = dash.Dash(__name__)

app.title = "AQI-GDP Dashboard"

def fetch_data(start_date, end_date, city=None):
    params = {'start_date': start_date, 'end_date': end_date, 'city': city}
    response = requests.get('http://127.0.0.1:5001/measurements', params=params)
    data = response.json()

    df = pd.json_normalize(data)

    # Convert 'timestamp' to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%a, %d %b %Y %H:%M:%S GMT')

    # Filter data based on date range
    mask = (df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)
    df = df.loc[mask]

    # Add a new column for marker colors
    conditions = [
        (df['aqi'] <= 50),
        (df['aqi'] <= 100),
        (df['aqi'] <= 150),
        (df['aqi'] <= 200),
        (df['aqi'] <= 300),
        (df['aqi'] > 300)
    ]
    choices = ['green', 'yellow', 'orange', 'red', 'purple', 'darkred']
    df['marker_color'] = np.select(conditions, choices, default='black')
    

    return df

city_select = {
    'Beijing': 'Beijing (北京)',    
    'Chicago': 'Chi_sp, Illinois, USA',  
    'London': 'London', 
    'Los Angeles': 'Los Angeles-North Main Street',
    'Mumbai': 'Mumbai US Consulate, India (मुंबई अमेरिकी वाणिज्य दूतावास)',
    'New York': 'New York',
    'São Paolo': 'Parque D.Pedro II, São Paulo, Brazil',
    'Shanghai': 'Shanghai (上海)',
    'Shenzhen': 'Shenzhen (深圳)',
    'Tokyo': 'Meguro (目黒)',  
}

# Layout of the app
app.layout = html.Div([
    html.H2("AQI of Global Cities with the Highest GDPs", 
            style={'textAlign': "center", 
                   'fontSize': 30, 
                   'fontFamily': 'Helvetica Neue', 
                   'fontWeight': 200}
           
    ),
    html.Div([
        dcc.DatePickerRange( 
            id='date-range-slider',
            min_date_allowed=date(2023, 5, 29), #Set dates based data available in Flask server
            max_date_allowed=date(2023, 6, 17),
            start_date=date(2023, 5, 29),
            end_date=date(2023, 6, 17),
        ),
    ], style={
        'text-align': 'right',  'margin-right': '9.5%'  
    }),
    dcc.Dropdown( #Dropdown selection
        id='group-dropdown',
        placeholder="Select group",
        options=[
            {'label': 'Global North Cities', 'value': 'g_north'},
            {'label': 'Global South Cities', 'value': 'g_south'}],
        value='all',  # default value
        style={'width': '90%', 
               'margin-left': '5%', 
               'margin-right': '5%', 
               'fontFamily': 'Helvetica Neue Light'}
    ),
    dcc.Dropdown(
        id='city-dropdown',
        placeholder="Select city",
        options=[{'label': name, 'value': city_select[name]} for name in city_select.keys()],
        multi=True,
        searchable=True,
        value=None,
        style={'width': '90%', 
               'margin-left': '5%', 
               'margin-right': '5%', 
               'fontFamily': 'Helvetica Neue Light'}
    ),

    html.Div([
    html.Div([
        html.H3('AQI Legend', style={'textAlign': 'left', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200,  'marginTop': '15px', 'marginBottom': '2px'}),       
        html.Div([
            html.Div(style={'backgroundColor': 'green', 'height': '20px', 'width': '80px'}),
            html.Div(style={'backgroundColor': 'yellow', 'height': '20px', 'width': '80px'}),
            html.Div(style={'backgroundColor': 'orange', 'height': '20px', 'width': '80px'}),
            html.Div(style={'backgroundColor': 'red', 'height': '20px', 'width': '80px'}),
            html.Div(style={'backgroundColor': 'purple', 'height': '20px', 'width': '80px'}),
            html.Div(style={'backgroundColor': 'darkred', 'height': '20px', 'width': '80px'}),
        ], style={'display': 'flex', 'justifyContent': 'left', 'marginTop': '2px', 'marginBottom': '0px'}),

        html.Div([
            html.P('0-50', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200, 'marginLeft': '20px', 'marginRight': '33px', 'marginTop': '2px', 'marginBottom': '0px'}),
            html.P('51-100', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue','fontWeight': 200, 'marginRight': '21px', 'marginTop': '2px', 'marginBottom': '0px'}),
            html.P('101-150', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200, 'marginRight': '12px', 'marginTop': '2px', 'marginBottom': '0px'}),
            html.P('151-200', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200, 'marginRight': '12px', 'marginTop': '2px', 'marginBottom': '0px'}),
            html.P('201-300', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200, 'marginRight': '20px', 'marginTop': '2px', 'marginBottom': '0px'}),
            html.P('>300', style={'fontSize': '18px', 'fontFamily': 'Helvetica Neue', 'fontWeight': 200, 'marginTop': '2px', 'marginBottom': '0px'}),
        ], style={'display': 'flex', 'justifyContent': 'left'}),
    ], style={'flex': '1'}),  # This element will take up the remaining space on the left side

    html.Div(
        dcc.RadioItems(
            id='map-style-toggle',
            options=[
                {'label': 'Light', 'value': 'mapbox://styles/mapbox/light-v10'}, #Mapbox token needed
                {'label': 'Dark', 'value': 'mapbox://styles/mapbox/dark-v11'} #Mapbox token needed
            ],
            value='mapbox://styles/mapbox/light-v10',  # default value
            style={'fontFamily': 'Helvetica Neue Light'},
        ), style={'text-align':'right', 'marginRight': '150px', 'marginTop': '50px'}
    ),
], style={'display': 'flex', 'marginLeft': '150px', 'marginBottom': '11px'}),




    #Map size and dimensions
    dcc.Graph(id='map-display', style={"height" : "80vh", "width" : "80%", 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    dcc.Graph(id='bar-display', style={"height" : "80vh", "width" : "80%", 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto'}),
    html.Br(),
    dcc.Graph(
        id='avg-aqi-graph',
        style={"height" : "60vh", "width" : "80%", 'display': 'block', 'marginLeft': 'auto', 'marginRight': 'auto'}),
    
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div([
        html.Br(),
        html.P([
            'This Dash application presents an interactive interface for visualizing Air Quality Index (AQI) data across different cities over time. The data is fetched via an API from the ',
            html.A('World Air Quality Index', href='https://waqi.info', target='_blank'), 
            ' and ingested into our PostgreSQL database. This database is then configured to our REST API using a Flask web server for retrieving and querying the AQI data. This dashboard represents the third layer where users can meaningfully interact with the AQI data. The map allows for time-sensitive, location-based visualizations. The color of mapped AQI points reflects the AQI of the median date from the date-range picker. The stacked bar graph represents AQI values for each city chronologically stacked by timestamp, with earlier timestamps at the bottom. By hovering over the map and graphs, users can get detailed information about specific AQI values at a particular timestamp. The comparative line graph averages the AQI values for the cities in each group. The aim of this dashboard is to provide near-real-time air quality information and insights, enabling users to understand the correlation between air quality and the economic urban powerhouses of the world. By raising awareness of air quality issues in these cities, the dashboard promotes a better understanding of the impact of air pollution on public health, environment, and the economy, driving efforts towards sustainable development and improved quality of life.'
        ], style={
               'margin-left': '200px', 
               'margin-right': '200px', 
               'text-align': 'justified', 
               'fontFamily': 'Helvetica Neue Light'
        }),

        html.Br(),
        html.P('This project was developed by Iyad Abdi, Filippo Bissi, and Valerio Paoloni and is a product of the course Software Engineering for Geoinformatics taken in the Spring semester of 2023 (A.Y. 2022-2023) at Politecnico di Milano under Professors Giovanni Quattrocchi & Daniele Oxoli.', 
               style={
                   'margin-left': '200px', 
                   'margin-right': '200px', 
                   'text-align': 'center', 
                   'fontFamily': 'Helvetica Neue Light'
               }),

        html.P([
        'For more information, visit our ',
        html.A('GitHub repo', href='https://github.com/fillobissi/la_botte', target='_blank'),
        '.'
        ], style={
               'margin-left': '200px', 
               'margin-right': '200px', 
               'text-align': 'center', 
               'fontFamily': 'Helvetica Neue Light'
        }),
        html.Br(),
    ], style={
        'backgroundColor': '#F2F4F5',

    }),

    
    html.Br(),
    
])

    



# Defining group-to-cities mapping
city_groups = {
    'all': ['Beijing', 'Chicago', 'London', 'Los Angeles', 'Mumbai', 'New York', 'São Paolo', 'Shanghai', 'Shenzhen', 'Tokyo'],
    'g_north': ['Chicago', 'London', 'Los Angeles', 'New York', 'Tokyo'],
    'g_south': ['Beijing', 'Mumbai', 'São Paolo', 'Shanghai', 'Shenzhen'],
}


# Update city options when group changes
@app.callback(
    Output('city-dropdown', 'options'),
    [Input('group-dropdown', 'value')]
)
def update_city_dropdown(group_dropdown_value):
    if group_dropdown_value in city_groups:
        cities = city_groups[group_dropdown_value]
    else:
        cities = list(city_select.keys())  # default to all cities

    options = [{'label': city, 'value': city_select[city]} for city in cities]
    return options


@app.callback(
    Output('group-dropdown', 'value'),
    [Input('city-dropdown', 'value')],
    [State('group-dropdown', 'value')]
)
def update_group_dropdown(city_dropdown_values, current_group):  # Treat this as list
    if city_dropdown_values is not None:
        selected_cities = [city for city, value in city_select.items() if value in city_dropdown_values]

        groups_for_selected_cities = set()  # a set to hold all unique groups for the selected cities
        for selected_city in selected_cities:
            for group, cities in city_groups.items():
                if selected_city in cities:
                    groups_for_selected_cities.add(group)
        
        # if all the selected cities belong to the same group, set that group
        if len(groups_for_selected_cities) == 1:
            return groups_for_selected_cities.pop()

        # if the selected cities belong to the current group, keep it
        if current_group in groups_for_selected_cities:
            return current_group

    # if no city is selected, or the selected cities belong to different groups, return 'all'
    return 'all'



@app.callback(
    Output('map-display', 'figure'),
    [Input('date-range-slider', 'start_date'),
     Input('date-range-slider', 'end_date'),
     Input('group-dropdown', 'value'),
     Input('city-dropdown', 'value'), 
     Input('map-style-toggle', 'value')]
)
def update_map(start_date, end_date, group_dropdown_value, city_dropdown_values, map_style):
    if city_dropdown_values:  # Treat this as list
        df = pd.DataFrame()
        for city_dropdown_value in city_dropdown_values:  # Iterate over list
            original_city_name = next(key for key, value in city_select.items() if value == city_dropdown_value)  # Get the original city name
            temp_df = fetch_data(start_date, end_date, original_city_name)
            df = pd.concat([df, temp_df])
    else:
        df = fetch_data(start_date, end_date)

    # Replace original city names with dictionary names
    reverse_city_select = {v: k for k, v in city_select.items()}
    df['city_name'] = df['city_name'].replace(reverse_city_select)

    # Filter the DataFrame to only include cities from the selected group
    if group_dropdown_value in city_groups and group_dropdown_value != 'all':
        df = df[df['city_name'].isin(city_groups[group_dropdown_value])]

    # Filter the DataFrame to only include the selected city
    if city_dropdown_values:  # Treat this as list
        df = df[df['city_name'].isin([reverse_city_select[value] for value in city_dropdown_values])]  # Iterate over list


    
    # Creating a copy of our original dataframe to add the size column
    temp_df = df.copy()
    temp_df['size'] = [25]*len(df)
    
    # Create the map
    fig = px.scatter_mapbox(
        temp_df, 
        lat="latitude", 
        lon="longitude",
        color="marker_color",
        color_discrete_map='identity',
        size='size', 
        hover_name='city_name',
        hover_data={
            "aqi": True,
            "timestamp": True,
            "marker_color": False,  # Hide from the hover data
            "latitude": False,  # Hide from the hover data
            "longitude": False,  # Hide from the hover data
            "size": False
        },
        zoom=1.1,
        center=dict(lat=25, lon=5)
    )
    
    #MAPBOX STYLES ACCESS TOKEN
    mapbox_access_token = os.getenv('MAPBOX_TOKEN')


    fig.update_layout(
        mapbox_style=map_style,
        mapbox_accesstoken=mapbox_access_token,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig

@app.callback(
    Output('bar-display', 'figure'),
    [Input('city-dropdown', 'value'),
     Input('group-dropdown', 'value'),
     Input('date-range-slider', 'start_date'),
     Input('date-range-slider', 'end_date')]
)
def update_bar_chart(city_dropdown_values, group_dropdown_value, start_date, end_date):

    # Check if specific cities are selected
    if city_dropdown_values:
        original_city_names = [next(key for key, value in city_select.items() if value == city) for city in city_dropdown_values]
        df_list = [fetch_data(start_date, end_date, city) for city in original_city_names]
        df = pd.concat(df_list)
    else:
        df = fetch_data(start_date, end_date)
    
    # Replace city names for plotting
    df['city_name'] = df['city_name'].replace({v: k for k, v in city_select.items()})
    
    # If a group but not a city is selected, filter data for that group
    if group_dropdown_value and group_dropdown_value != 'all':
        group_cities = []
        for group, cities in city_groups.items():
            if group == group_dropdown_value:
                group_cities.extend(cities)
        df = df[df['city_name'].isin(group_cities)]
    
    # If specific cities are selected, filter data for those cities
    if city_dropdown_values:
        df = df[df['city_name'].isin(original_city_names)]
    
    
    conditions = [
        (df['aqi'] <= 50),
        (df['aqi'] <= 100),
        (df['aqi'] <= 150),
        (df['aqi'] <= 200),
        (df['aqi'] <= 300),
        (df['aqi'] > 300)
    ]
    choices = ['0-50', '51-100', '101-150', '151-200', '201-300', '>300']
    df['AQI range'] = np.select(conditions, choices, default='black')

    # Ensure the timestamp is datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Define colors
    color_discrete_map={
                    '0-50': 'green',
                    '51-100': 'yellow',
                    '101-150': 'orange',
                    '151-200': 'red',
                    '201-300': 'purple',
                    '>300': 'darkred'
                }
    
    # Initialize figure
    fig = go.Figure()

    # Get unique dates
    unique_dates = np.sort(df['timestamp'].unique())

    # Generate bar chart for each unique date
    for date in unique_dates:
        temp_df = df[df['timestamp'] == date]
        fig.add_trace(go.Bar(
            x=temp_df['city_name'],
            y=temp_df['aqi'],
            marker_color=temp_df['AQI range'].map(color_discrete_map),
            name=str(date),
            showlegend=False
        ))

    fig.update_layout(
        title="Stacked Chronological AQI Levels by City",
        xaxis_title="City",
        yaxis_title="Stacked Air Quality Index (AQI) Readings",
        barmode='stack',
        font_size=14, 
        font_family="Helvetica Neue Light",
        plot_bgcolor='#ECEFF1',  
        paper_bgcolor='#ffffff'
    )

    return fig





@app.callback(
    Output('avg-aqi-graph', 'figure'),
    [Input('date-range-slider', 'start_date'),
     Input('date-range-slider', 'end_date')]
)
def update_avg_aqi_graph(start_date, end_date):
    df = fetch_data(start_date, end_date)
    
    # Replace city names
    reverse_city_select = {v: k for k, v in city_select.items()}
    df['city_name'] = df['city_name'].replace(reverse_city_select)

    # Calculate the average AQIs for global north and global south
    df_north = df[df['city_name'].isin(city_groups['g_north'])]
    df_south = df[df['city_name'].isin(city_groups['g_south'])]

    df_north = df_north.groupby(df_north.timestamp.dt.date).mean().round(2).reset_index()
    df_south = df_south.groupby(df_south.timestamp.dt.date).mean().round(2).reset_index()
    
    # Create line chart with Plotly Express
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_north['timestamp'], y=df_north['aqi'],
                    mode='lines',
                    name='Global North'))
    fig.add_trace(go.Scatter(x=df_south['timestamp'], y=df_south['aqi'],
                    mode='lines',
                    name='Global South'))
    
    fig.update_layout(
        title='Comparison of Average AQI of Global North and Global South Cities Over Time',
        xaxis_title='Time period',
        yaxis_title='Average AQI',
        font_size=14, 
        font_family="Helvetica Neue Light",
        plot_bgcolor='#F2F4F5',  
        paper_bgcolor='#F2F4F5' 
         
    )

    
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




