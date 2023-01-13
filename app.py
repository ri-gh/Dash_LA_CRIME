import pandas as pd
import plotly.express as px
import dash
from dash import html, dash_table
from dash import dcc
import datetime

df = pd.read_csv("LA_Crime_clean.csv")

list_area = df['AREA NAME'].unique().tolist()
list_year = df['year'].unique().tolist()
list_month = df['month_name'].unique().tolist()
list_month = sorted(list_month, key=lambda t: datetime.datetime.strptime(t,'%B')) #to sort the list by month ranking and not alphabetic way
list_day_name = df['day_name'].unique().tolist()
list_hour = df['hour'].unique().tolist()
list_date = df['DATE OCC'].unique().tolist()


app = dash.Dash(__name__)

app.layout = html.Div(children=[ 
    html.Div(children=html.H3(children="Select your area:")),
    dcc.Dropdown(id="select-area",
    options=sorted([{"label": area, "value":area} for area in list_area], key = lambda x: x['label']),
    value="",
    multi = True,
    placeholder='Select an area...'),
    html.Div(id="year-select-div"),
    dcc.Dropdown(id="select-year",
    options=sorted([{"label": year, "value":year} for year in list_year], key = lambda x: x['label']),
    value="",
    multi = False,
    placeholder='Select a year...'),

    html.Div(id="month-select-div"),
    dcc.Dropdown(id="select-month",
    options = [month for month in list_month], #we didn't sorted the month alphabetically because we already sorted them by them ranking upper
    value="",
    multi = False,
    placeholder='Select a month...'),

     
    dcc.RangeSlider(min(list_hour),max(list_hour), 1, value=[0,1], allowCross=False,
    tooltip={"placement": "top", "always_visible": False},
    marks={0:{'label':'00:00', 'style': {'color': '#77b0b1'}},
    1:{'label':'01:00'},
    2:{'label':'02:00'},
    3:{'label':'03:00'},
    4:{'label':'04:00'},
    5:{'label':'05:00'},
    6:{'label':'06:00'},
    7:{'label':'07:00'},
    8:{'label':'08:00'},
    9:{'label':'09:00'},
    10:{'label':'10:00'},
    11:{'label':'11:00'},
    12:{'label':'12:00'},
    13:{'label':'13:00'},
    14:{'label':'14:00'},
    15:{'label':'15:00'},
    16:{'label':'16:00'},
    17:{'label':'17:00'},
    18:{'label':'18:00'},
    19:{'label':'19:00'},
    20:{'label':'20:00'},
    21:{'label':'21:00'},
    22:{'label':'22:00'},
    23:{'label':'23:00','style': {'color': '#f50'}},
    },

    id='my_range_slider'),
  
    #html.Div(id='output-container-range-slider'),
    dcc.Graph(id='graph_area_year'),
    dcc.Graph(id='graph_area_year_hour'),
    dcc.Graph(id='graph_area_year_global'),
    dcc.Graph(id="graph_area_month_global"),
    dcc.Graph(id="graph_LA_month_global"),
    dcc.Graph(id="graph_area_month_global_crime"),
    dcc.Graph(id="graph_area_crime_hour")

     ]
)

@app.callback(dash.dependencies.Output("year-select-div", "children"),
    dash.dependencies.Input("select-area", "value"))
def display_name_dept(area):
    # We return an H3 HTML component with the name of the area.
    return html.H3(children="Select a year for {}".format(area))

@app.callback(dash.dependencies.Output("month-select-div", "children"),
    dash.dependencies.Input("select-year", "value"))
def display_name_dept(year):
    # We return an H3 HTML component with the name of the area.
    return html.H3(children="Choose a month for year {}".format(year))


'''@app.callback(dash.dependencies.Output("output-container-range-slider", "children"),
    dash.dependencies.Input("select-month", "value"),
    dash.dependencies.Input("select-year", "value"),
    dash.dependencies.Input("select-area", "value"),
    dash.dependencies.Input('my_range_slider', 'value'))

def info_return(month_choose,year_choose,area,hour_choice):

    return  month_choose,year_choose,area,hour_choice[0], hour_choice[1]'''


@app.callback(dash.dependencies.Output("graph_area_year", "figure"),
    dash.dependencies.Output("graph_area_year_hour", "figure"),
    dash.dependencies.Output("graph_area_year_global", "figure"),
    dash.dependencies.Output("graph_area_month_global", "figure"),
    dash.dependencies.Output("graph_LA_month_global", "figure"),
    dash.dependencies.Output("graph_area_month_global_crime", "figure"),
    dash.dependencies.Output("graph_area_crime_hour", "figure"),
    dash.dependencies.Input("select-month", "value"),
    dash.dependencies.Input("select-year", "value"),
    dash.dependencies.Input("select-area", "value"),
    dash.dependencies.Input('my_range_slider', 'value'))

def area_map(month_choose, year_choose,area,hour_choice):
    df_area = df[df['AREA NAME'].isin(area)].reset_index(drop=True) #to put several areas from the dropdown
    df_area = df_area[df_area['year'] == year_choose].reset_index(drop=True)
    df_area = df_area[df_area['month_name'] == month_choose].reset_index(drop=True)

    df_line = df_area
    df_plot_line = df_line.groupby(['AREA NAME','hour'])['Crm Cd Desc'].count()
    df_plok =  pd.DataFrame(df_plot_line)
    df_plok= df_plok.reset_index() # to have the multi-index data as columns of this df

    fig_line = px.line(df_plok, x="hour", y='Crm Cd Desc', color='AREA NAME',
        title= "Total crime number evolution per hour for LA's area in {} {}".format(month_choose,year_choose),
        custom_data=['AREA NAME','hour','Crm Cd Desc'])
    fig_line.update_layout(legend_title_text= "LA's area:",
    xaxis_title="Hours",
        yaxis_title="Number of crime")
    fig_line.update_traces(
         hovertemplate="<br>".join([
        "Area: %{customdata[0]}",
        "Period: {} {}".format(month_choose,year_choose),
        "Hour: %{customdata[1]}",
        "Total crime number: %{customdata[2]}"
        ])
    )
    df_plot_bar = df_line.groupby('AREA NAME')['Crm Cd Desc'].count()
    df_plot_bar = pd.DataFrame(df_plot_bar)
    df_plot_bar = df_plot_bar.reset_index()

    fig_bar = px.bar(df_plot_bar,x='AREA NAME', y='Crm Cd Desc',color='AREA NAME',
    title="Global crime figures for {} {} in LA's area ".format(month_choose,year_choose),
    custom_data=['AREA NAME','Crm Cd Desc'])
    fig_bar.update_layout(legend_title_text= "LA's area:",
    xaxis_title="Area",
    yaxis_title="Number of crime")
    fig_bar.update_traces(hovertemplate="<br>".join([
    "Area: %{customdata[0]}",
    "Period: {} {}".format(month_choose,year_choose),
    "Total number of crime: %{customdata[1]}"]))

    start_hour = hour_choice[0] #to have the first hour selected from the range slider
    end_hour = hour_choice[1]   #to have the last hour selected from the range slider
    df_area = df_area[(df_area['hour'] >=  start_hour) & (df_area['hour'] < end_hour)].reset_index(drop=True)


    fig = px.scatter_mapbox(df_area, lat="LAT", lon="LON",color='AREA NAME',size= 'Vict Age',mapbox_style="open-street-map",
    title="LA's areas crime map for {} {} between {}h and {}h".format(month_choose, year_choose,start_hour,end_hour),
    custom_data=['AREA NAME','Vict Age','Vict Sex','Vict Descent','Crm Cd Desc','TIME OCC','DATE OCC','LOCATION'],
    center={'lat': 34.052235, 'lon': -118.243683},#to center the map on LA
    zoom=7)
    fig.update_traces(
    hovertemplate="<br>".join([
        "Area Name: %{customdata[0]}",
        "Victim age : %{customdata[1]}",
        "Victim Sex : %{customdata[2]}",
        "Victim Descent : %{customdata[3]}",
        "Crime description : %{customdata[4]} ",
        "Time : %{customdata[5]}",
        "Date occured : %{customdata[6]}",
        "Location : %{customdata[7]} "
    ])
    )

    df_line_month = df[(df['month_name'] == month_choose) | (df['year'] == year_choose)].reset_index(drop=True)
    df_line_month = df_line_month.groupby('hour')['Crm Cd Desc'].count()
    df_line_month = pd.DataFrame(df_line_month)
    df_line_month = df_line_month.reset_index()
    fig_line_month = px.bar(df_line_month,x='hour', y='Crm Cd Desc',color= 'hour',
    title="Global sum of crime per hour in LA for {} {}".format(month_choose,year_choose))
    fig_line_month.update_layout(legend_title_text= "LA's area:",
    xaxis_title="Time",
    yaxis_title="Number of crime")
    '''fig_line_month = px.line(df_line_month, x="hour", y='Crm Cd Desc',
    title='Evolution of crime number per hour in LA for {} {}'.format(month_choose,year_choose))'''

    df_global_per_year = df[df['year'] == year_choose].reset_index(drop=True)
    df__month_plot = df_global_per_year.groupby('month_name')['Crm Cd Desc'].count()
    df__month_plot = pd.DataFrame(df__month_plot)
    df__month_plot = df__month_plot.reset_index()
    df__month_plot['month_name'] = sorted(df__month_plot['month_name'], key=lambda t: datetime.datetime.strptime(t,'%B'))

    fig_month_line = px.line(df__month_plot, x="month_name", y='Crm Cd Desc',
    title="Evolution of crime number per month in {} for LA".format(year_choose))
    fig_month_line.update_layout(xaxis_title="Month",
    yaxis_title="Number of crime")

    df_line_area = df[(df['month_name'] == month_choose) | (df['year'] == year_choose)].reset_index(drop=True)
    df_line_area = df_line_area.groupby('AREA NAME')['Crm Cd Desc'].count()
    df_line_area = pd.DataFrame(df_line_area)
    df_line_area = df_line_area.reset_index()
    fig_line_area = px.bar(df_line_area,x='AREA NAME', y='Crm Cd Desc',color= 'AREA NAME',
    title="Global sum of crime per area in LA for {} {}".format(month_choose,year_choose))
    fig_line_area.update_layout(legend_title_text= "LA's area:",
    xaxis_title="Area name",
    yaxis_title="Number of crime")

    df_crime_per_hour = df[(df['year'] == year_choose)|(df['month_name'] == month_choose)]
    df_crime_per_hour = df_crime_per_hour[(df_crime_per_hour['hour'] >=  start_hour) & (df_crime_per_hour['hour'] < end_hour)].reset_index(drop=True)
    df_crime_per_hour = pd.DataFrame(df_crime_per_hour.groupby('AREA NAME')['Crm Cd Desc'].count()).reset_index()

    fig_crime_per_area = px.bar(df_crime_per_hour,x='AREA NAME', y='Crm Cd Desc',color= 'Crm Cd Desc',
    title="Global sum of crime per area in LA for {} {} between {} h and {} h".format(month_choose,year_choose,start_hour,end_hour))
    fig_crime_per_area.update_layout(xaxis={'categoryorder':'total descending'}, #to order the bar by descending value
    xaxis_title="Area name",
    yaxis_title="Number of crime")


    return   fig, fig_line, fig_line_month,fig_bar,fig_month_line ,fig_line_area , fig_crime_per_area

if __name__=="__main__":
    app.run_server(debug=True)