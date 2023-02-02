import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
import datetime
import dash_bootstrap_components as dbc


df = pd.read_csv("your_file_path\\LA_Crime_clean.csv")


logo ='https://i.pinimg.com/736x/7d/21/ab/7d21ab6fbc01448ffdedb319c8389977.jpg'

logo_dash = 'https://avatars0.githubusercontent.com/u/5997976?s=400&v=4'


list_area = df['AREA NAME'].unique().tolist()
list_year = df['year'].unique().tolist()
list_month = df['month_name'].unique().tolist()
list_month = sorted(list_month, key=lambda t: datetime.datetime.strptime(t,'%B')) #to sort the list by month ranking and not alphabetic way
list_hour = df['hour'].unique().tolist()

#Show a default graph when opening the dash app we create a default df for Hollywood in May 2020 between 5 & 8 am:
month_choose = 'May'
year_choose = 2020
area = 'Hollywood'
df_default = df[df['year'] == year_choose].reset_index(drop=True)
df_default = df_default[df_default['month_name'] == month_choose].reset_index(drop=True)
df_default = df_default[df_default['AREA NAME'] == area].reset_index(drop=True)
start_hour = 5 #to have the first hour selected from the range slider
end_hour = 8   #to have the last hour selected from the range slider
df_default = df_default[(df_default['hour'] >=  start_hour) & (df_default['hour'] <= end_hour)].reset_index(drop=True)
df_default = df_default.reset_index(drop=True)

def default_pie(): 
    df_pie_default = df_default.groupby('Type of crime')['Crm Cd Desc'].count()
    df_pie_default = df_pie_default.reset_index()
    df_pie_default = pd.DataFrame(df_pie_default)

    fig_pie_default = px.pie(df_pie_default,values='Crm Cd Desc',names='Type of crime',
    title='Repartition of crime type for {} area'.format(area))
    fig_pie_default.update_traces(textposition='inside', textinfo='percent+label',#to put the label inside the pie
    hovertemplate="<br>".join(["Period: {} {}".format(month_choose,year_choose),
        "Hours range: between {}h and {}h".format(start_hour,end_hour),
        "Type of crime: %{label}",
        "Number: %{value}"] ))
    fig_pie_default.update_traces(hole=.4) #to change the pie chart to donut chart
    fig_pie_default.update_layout(legend_title_text= "Type of crime:",
    template='plotly_dark',
    legend=dict(font=dict(color="white")), #to change color of the legend 
    title_font_color="rgb(159, 241, 253)", #to change the color of the figure title
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph

    return fig_pie_default


def default_bar():
    df_line_day_name = df_default.groupby(['AREA NAME','month_name','year','day_name','day_ranking'])['Crm Cd Desc'].count().reset_index()
    df_line_day_name = pd.DataFrame(df_line_day_name)
    df_line_day_name = df_line_day_name.sort_values('day_ranking').reset_index()

    fig_day_name_area_default = px.bar(df_line_day_name,x='day_name', y='Crm Cd Desc',color= 'AREA NAME',
    title="Sum of crime per day name and area")
    fig_day_name_area_default.update_traces(
        hovertemplate="<br>".join(["Day of the week: %{x}",
        "Period : {} {} ".format(df_line_day_name['month_name'][0],df_line_day_name['year'][0]),
        "Range of hour: between {}h and {}h".format(start_hour,end_hour),
        "Number of crime: %{y}"] ))
    fig_day_name_area_default.update_xaxes(color="rgb(159, 241, 253)",showgrid = False) #change color of xaxes labels
    fig_day_name_area_default.update_yaxes(color="white") #change color of yaxes labels
    fig_day_name_area_default.update_layout(legend_title_text= "Area:",
    xaxis_title="May 2020 between 5h and 8h",
    yaxis_title="Number of crime",
    template='plotly_dark',
    legend=dict(font=dict(color="white")), 
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph

    return fig_day_name_area_default

def default_fig_line():
    df_plot_line = df_default.groupby(['AREA NAME','hour'])['Crm Cd Desc'].count()
    df_plok =  pd.DataFrame(df_plot_line)
    df_plok= df_plok.reset_index() # to have the multi-index data as columns of this df

    fig_line_default = px.line(df_plok, x="hour", y='Crm Cd Desc', color='AREA NAME',
    title= "Crime number per hour between 5h and 8h in May 2020",
    custom_data=['AREA NAME','hour','Crm Cd Desc'])
    fig_line_default.update_layout(legend_title_text= "Area:",
    xaxis_title="Hours",
    yaxis_title="Number of crime",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig_line_default.update_traces(
        hovertemplate="<br>".join([
    "Area: %{customdata[0]}",
    "Period: May 2020",
    "Hour: %{customdata[1]}",
    "Total crime number: %{customdata[2]}"
        ])
    )
    fig_line_default.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
    fig_line_default.update_yaxes(color="white") #change color of yaxes labels

    return fig_line_default

def default_fig():
    fig_default = px.scatter_mapbox(df_default, lat="LAT", lon="LON",color='AREA NAME',size= 'Vict Age',mapbox_style="carto-darkmatter",
    title="LA's areas crime map for May 2020 between 5h and 8h",
    custom_data=['AREA NAME','Vict Age','Vict Sex','Crm Cd Desc','TIME OCC','DATE OCC','LOCATION'],
    center={'lat': 34.052235, 'lon': -118.243683},#to center the map on LA
    zoom=6)
    fig_default.update_traces(
    hovertemplate="<br>".join([
        "Area Name: %{customdata[0]}",
        "Victim age : %{customdata[1]}",
        "Victim Sex : %{customdata[2]}",
        "Crime description : %{customdata[3]} ",
        "Time : %{customdata[4]}",
        "Date occured : %{customdata[5]}",
        "Location : %{customdata[6]} "
    ])
    )
    fig_default.update_layout(legend_title_text= "Area:",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig_default.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig_default.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig_default

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

app.layout = html.Div([
    dbc.Card(dbc.CardBody([
    html.Br(),
    dbc.Row([
        html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([html.Img(src=logo, height="150px"),
                html.P(),
                    
                            dbc.Row(
                [ html.H2("Los Angeles areas crime report analysis from 2020 until today",style={'textAlign': 'center'}), #to add an header text line  #logo
                    dbc.Col(),

                ])], style={'textAlign': 'center',
                'color':'rgb(159, 241, 253)', 'background-color':'black'},                #to change color of the written font

                )
                

            ],style={'background-color':'dark'})
        ),
    ],style={'background-color':'dark'}),
    ]),
    dbc.Row([
    dbc.Col([dbc.Button(html.Div(children=[ 
    html.Div(children=html.H5(children="Select year:"),style={'color':'rgb(159, 241, 253)'}),
    dcc.Dropdown(
    options=sorted([{"label": year, "value":year} for year in list_year], key = lambda x: x['label']),
    value='',
    multi = False,
    style={'color': 'Blue','background-color':'rgb(159, 241, 253)'},
    placeholder='Select a year...',
    id="select-year"),
    html.Div(id="month-select-div",style={'color':'rgb(159, 241, 253)'}),
    dcc.Dropdown(id="select-month",
    options = [month for month in list_month], #we didn't sorted the month alphabetically because we already sorted them by them ranking upper
    value='',
    multi = False,
    style={'color': 'Blue','background-color':'rgb(159, 241, 253)'},
    placeholder='Select a month...'),

    html.Br(),
    html.Div(id="select-hour-div",style={'color':'rgb(159, 241, 253)'}),
    dcc.RangeSlider(min(list_hour),max(list_hour),1,allowCross=False,
    tooltip={"placement": "top", "always_visible": False},
    marks={0:{'label':'00', 'style': {'color': '#77b0b1'}},
    1:{'label':'01'},
    2:{'label':'02'},
    3:{'label':'03'},
    4:{'label':'04'},
    5:{'label':'05'},
    6:{'label':'06'},
    7:{'label':'07'},
    8:{'label':'08'},
    9:{'label':'09'},
    10:{'label':'10'},
    11:{'label':'11'},
    12:{'label':'12'},
    13:{'label':'13'},
    14:{'label':'14'},
    15:{'label':'15'},
    16:{'label':'16'},
    17:{'label':'17'},
    18:{'label':'18'},
    19:{'label':'19'},
    20:{'label':'20'},
    21:{'label':'21'},
    22:{'label':'22'},
    23:{'label':'23','style': {'color': '#f50'}},
    },

    id='my_range_slider'),

    html.Br(),
    html.Div(id="space"),
    html.Br(),
    dcc.Dropdown(
    options=sorted([{"label": area, "value":area} for area in list_area], key = lambda x: x['label']),
    value='',
    multi = True,
    style={'color': 'Blue','background-color':'rgb(159, 241, 253)'},
    placeholder='Select area...',
    id="select-area"),
  
    dcc.Checklist(id='select-all',                        #to add a select all tick box
    options=[{'label': 'Select all areas', 'value': 1}]),
    ],style={'background-color':'black'},
    ),
    style={"width":"100%","height": "100%",'color':'rgb(159, 241, 253)'})],width=4, #layout width are between 0 & 12
    align='center'), 

    
    dbc.Col([dbc.Button(dcc.Graph(id="graph_area_fig_pie",figure=default_pie()),style={"width":"100%","height": "100%"})],width=4,
    align='center'),
    #to set up height of the component
    dbc.Col([dbc.Button(dcc.Graph(id="graph_day_name_area",figure=default_bar()),style={"width": "100%","height": "100%"})],width=4),
    ], align='center'),
    html.Br(),
    dbc.Row([
    dbc.Col([dbc.Button(dcc.Graph(id="graph_per_hour_line",figure=default_fig_line()), style={"width": "100%","height": "100%"})],width=6,
    align='center'),
    dbc.Col([dbc.Button(dcc.Graph(id="graph_per_hour_map",figure=default_fig()),style={"width": "100%","height": "100%"})],width=6)
    ], align='center'),
]), color = 'dark'
    ),
        html.Br(),
    dbc.Row([
        dbc.Col([dbc.Button(html.Img(src=logo_dash, height="50px"),style={'color':'black',"width": "100%","height": "100%", "textAlign" :"left",
        'background-color':'black'})
            ],style={'color':'black','background-color':'black'})

    ],style={'color':'black','background-color':'black'}) ],style={'color':'black','background-color':'black'})


@app.callback(dash.dependencies.Output("month-select-div", "children"),
    dash.dependencies.Input("select-year", "value"))
def display_year(year):
    # We return an H5 HTML component with the name of the year.
    return html.H5(children="Select a month in {} :".format(year))

@app.callback(dash.dependencies.Output("select-hour-div", "children"),
        dash.dependencies.Input('select-month', "value"),
        dash.dependencies.Input("select-year", "value"))
def display_month_year(month, year):
    # We return an H5 HTML component with the name of the month & year.
    return html.H5(children="Select a range of hours in {} {}:".format(month,year))


@app.callback(dash.dependencies.Output("my_range_slider", "children"),
        dash.dependencies.Input("my_range_slider", "value"))
def display_hour_range(hour_choice):
    # We return an H5 HTML component with the range of hour selected upper.
    return html.P(),html.Br(),html.H5(children="Select area between {}h and {}h :".format(hour_choice[0],hour_choice[1]))

#to add a select all tick box
@app.callback(
    dash.dependencies.Output('select-area', 'value'),
    [dash.dependencies.Input('select-all', 'value')],
    dash.dependencies.State('select-area', 'options'),
     )
def test(selected, options):
    if selected[0] == 1:
        return [i['value'] for i in options]
    else:
        return options

@app.callback(
    dash.dependencies.Output("graph_area_fig_pie", "figure"),
    dash.dependencies.Output("graph_day_name_area", "figure"),
    dash.dependencies.Output("graph_per_hour_line", "figure"),
    dash.dependencies.Output("graph_per_hour_map", "figure"),
    dash.dependencies.Input("select-month", "value"),
    dash.dependencies.Input("select-year", "value"),
    dash.dependencies.Input("select-area", "value"),
    dash.dependencies.Input('my_range_slider', 'value'))

def pie(month_choose, year_choose,area,hour_choice):
    df_area = df[df['year'] == year_choose].reset_index(drop=True)
    df_area = df_area[df_area['month_name'] == month_choose].reset_index(drop=True)
    df_area = df_area[df_area['AREA NAME'].isin(area)].reset_index(drop=True)


    start_hour = hour_choice[0] #to have the first hour selected from the range slider
    end_hour = hour_choice[1]   #to have the last hour selected from the range slider
    df_area = df_area[(df_area['hour'] >=  start_hour) & (df_area['hour'] <= end_hour)].reset_index(drop=True)

    df_pie_area = df_area.groupby('Type of crime')['Crm Cd Desc'].count()
    df_pie_area = pd.DataFrame(df_pie_area)
    df_pie_area = df_pie_area.reset_index()
    fig_pie = px.pie(df_pie_area,values='Crm Cd Desc',names='Type of crime',
    title='Repartition of crime type for all selected area')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label',#to put the label inside the pie
    hole=.4,
    hovertemplate="<br>".join(["Period: {} {}".format(month_choose,year_choose),
        "Hours range: between {}h and {}h".format(start_hour,end_hour),
        "Type of crime: %{label}",
        "Number: %{value}"] ))
    fig_pie.update_layout(legend_title_text= "Type of crime:",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig_pie.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig_pie.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    df_line_day_name = df_area.groupby(['AREA NAME','month_name','year','day_name','day_ranking'])['Crm Cd Desc'].count().reset_index()
    df_line_day_name = pd.DataFrame(df_line_day_name)
    df_line_day_name = df_line_day_name.sort_values('day_ranking').reset_index(drop=True)

    fig_day_name_area = px.bar(df_line_day_name,x='day_name', y='Crm Cd Desc',color= 'AREA NAME',
    title="Sum of crime per day name and area")
    fig_day_name_area.update_traces(
        hovertemplate="<br>".join(["Day of the week: %{x}",
        'Period: {} {}'.format(month_choose,year_choose),
        'Range of hours: between {}h and {}h'.format(start_hour,end_hour),
        "Number of crime: %{y}"] ))
    fig_day_name_area.update_layout(legend_title_text= "Area:",
    xaxis_title="{} {} between {}h and {}h".format(month_choose,year_choose,start_hour,end_hour),
    yaxis_title="Number of crime",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig_day_name_area.update_xaxes(color="rgb(159, 241, 253)") #change color of xaxes labels
    fig_day_name_area.update_yaxes(color="white") #change color of yaxes labels

    df_plot_line = df_area.groupby(['AREA NAME','hour'])['Crm Cd Desc'].count()
    df_plok =  pd.DataFrame(df_plot_line)
    df_plok= df_plok.reset_index() # to have the multi-index data as columns of this df

    fig_line = px.line(df_plok, x="hour", y='Crm Cd Desc', color='AREA NAME',
    title= "Crime number per hour between {}h and {}h in {} {}".format(start_hour,end_hour,month_choose,year_choose),
    custom_data=['AREA NAME','hour','Crm Cd Desc'])
    fig_line.update_layout(legend_title_text= "Area:",
    xaxis_title="Hours",
    yaxis_title="Number of crime",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig_line.update_traces(
        hovertemplate="<br>".join([
    "Area: %{customdata[0]}",
    "Period: {} {}".format(month_choose,year_choose),
    "Hour: %{customdata[1]}",
    "Total crime number: %{customdata[2]}"
        ])
    )
    fig_line.update_xaxes(color="rgb(159, 241, 253)")#change color of xaxes labels
    fig_line.update_yaxes(color="white") #change color of yaxes labels

    fig = px.scatter_mapbox(df_area, lat="LAT", lon="LON",color='AREA NAME',size= 'Vict Age',mapbox_style="carto-darkmatter",
    title="LA's areas crime map for {} {} between {}h and {}h".format(month_choose, year_choose,start_hour,end_hour),
    custom_data=['AREA NAME','Vict Age','Vict Sex','Crm Cd Desc','TIME OCC','DATE OCC','LOCATION'],
    center={'lat': 34.052235, 'lon': -118.243683},#to center the map on LA
    zoom=6)
    fig.update_traces(
    hovertemplate="<br>".join([
        "Area Name: %{customdata[0]}",
        "Victim age : %{customdata[1]}",
        "Victim Sex : %{customdata[2]}",
        "Crime description : %{customdata[3]} ",
        "Time : %{customdata[4]}",
        "Date occured : %{customdata[5]}",
        "Location : %{customdata[6]} "
    ])
    )
    fig.update_layout(legend_title_text= "Area:",
    template='plotly_dark',
    title_font_color="rgb(159, 241, 253)",
    paper_bgcolor='black', #to change the background color of the figure
    plot_bgcolor='black')#to change the background colour of the graph
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)

    return fig_pie, fig_day_name_area, fig_line, fig


if __name__ == "__main__":
    app.run_server(debug=True)
