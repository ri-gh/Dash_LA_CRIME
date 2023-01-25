import dash
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
import datetime
import os

url='https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD'


df = pd.read_csv(url)
#we take a sample of the df because it'll be too heavy for deployment
df = df.sample(50000)

#We are going to add a column 'Type of crime' to categorize each crime description given by key word
#We instanciate a list of key word for crime
vandalism = ['VANDALISM']
list_of_crime_sex =['SEX','RAPE','INCEST','INDECENT','HUMAN','PANDERING','BIGAMY','LEWD','PIMPING','ORAL COPULATION']
list_of_crime_theft = ['THEFT','ROBBERY','BURGLARY','STOLEN','VEHICLE','PICKPOCKET','DRIVING WITHOUT OWNER CONSENT (DWOC)','SNATCH','SHOPLIFTING','EXTORTION']
simple_assault = ['SIMPLE ASSAULT']
aggravated_assault = ['AGGRAVATED ASSAULT']

#here s a list for the remaining crime:
crime_categoy_desc_list = vandalism + list_of_crime_sex+ list_of_crime_theft+ simple_assault+aggravated_assault

#we create several df where crime description contains the listed key word
df_vandalism = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(vandalism)))]
df_vandalism['Type of crime'] = 'Vandalism'

df_sex_crime = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(list_of_crime_sex)))]
df_sex_crime['Type of crime'] = 'Sex crime'

df_theft_crime = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(list_of_crime_theft)))]
df_theft_crime['Type of crime'] = 'Theft'

df_simple_assault = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(simple_assault)))]
df_simple_assault['Type of crime'] = 'Simple assault'

df_aggravated_assault = df[df['Crm Cd Desc'].str.contains('{}'.format('|'.join(aggravated_assault)))]
df_aggravated_assault['Type of crime'] = 'Aggravated assault'

#the columns not containing one of the crime description keyword listed upper will be tagged as type 'other'
df_other_crime = df[~df['Crm Cd Desc'].str.contains('{}'.format('|'.join(crime_categoy_desc_list)))]
df_other_crime['Type of crime'] = 'other'

#we'll append the full df with the new column 'Type of crime' & comments added inside
df_to_append = [df_sex_crime ,df_theft_crime , df_simple_assault, df_aggravated_assault,df_vandalism]

df_global = df_other_crime.append(df_to_append)
df_global = df_global.reset_index(drop=True)

#to show %age of null values bor each column
percentage_null_value =df_global.isnull().sum()/df_global.shape[0]*100
percentage_null_value.sort_values(ascending=False)

#we'll remove columns we more than 50% of missing values
col_to_remove = []
for i in range (len(percentage_null_value)):
    if percentage_null_value.values[i] > 50:
        col_to_remove.append(percentage_null_value.index[i])


df = df_global.drop(labels = col_to_remove, axis=1)

df = df.fillna("unkown")

#reformating the date data:

df['Date Rptd'] = df['Date Rptd'].str.split(' ',expand=True)[0]
df['DATE OCC'] = df['DATE OCC'].str.split(' ',expand=True)[0]
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'])

df['TIME OCC'] = pd.to_datetime(df['TIME OCC'].astype(str).str.zfill(4), format='%H%M')

#to get unique values count for each column to remove the uninteristing ones:
pd.DataFrame(df.nunique())

#we remove the below columns with too much useless data(redundancy, not signifiant data):
df = df.drop(labels=['DR_NO','Part 1-2','AREA','Crm Cd','Crm Cd 1','Premis Cd','Status','Mocodes'],axis=1)


#create & extract year / month/ day / day-name / hour from existing date columns
df['year']= df['DATE OCC'].dt.year
df['month']= df['DATE OCC'].dt.month
df['month_name']= df['DATE OCC'].dt.month_name()
df['day']= df['DATE OCC'].dt.day
df['day_name']= df['DATE OCC'].dt.day_name()
df['hour'] = df['TIME OCC'].dt.hour

df['TIME OCC'] = df['TIME OCC'].astype(str).str.split(' ' , expand=True)[1]


logo = 'https://www.pngfind.com/pngs/m/598-5981711_city-of-los-angeles-crest-transparent-city-of.png'

logo_dash = 'https://avatars0.githubusercontent.com/u/5997976?s=400&v=4'


list_area = df['AREA NAME'].unique().tolist()
list_year = df['year'].unique().tolist()
list_month = df['month_name'].unique().tolist()
list_month = sorted(list_month, key=lambda t: datetime.datetime.strptime(t,'%B')) #to sort the list by month ranking and not alphabetic way
list_hour = df['hour'].unique().tolist()

#to not show default graph when opening the dash app
def blank_fig(): 
    fig_blank = px.line(None, x= None, y = None)
    fig_blank.update_layout(template = 'plotly_dark')
    fig_blank.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig_blank.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig_blank


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
                'color':'white'},                #to change color of the written font

                )
                

            ])
        ),
    ]),
    ]),
    dbc.Row([
    dbc.Col([dbc.Button(html.Div(children=[ 
    html.Div(children=html.H5(children="Select year:")),
    dcc.Dropdown(id="select-year",
    options=sorted([{"label": year, "value":year} for year in list_year], key = lambda x: x['label']),
    value='',
    multi = False,
    placeholder='Select a year...'),
    html.Div(id="month-select-div"),
    dcc.Dropdown(id="select-month",
    options = [month for month in list_month], #we didn't sorted the month alphabetically because we already sorted them by them ranking upper
    value='',
    multi = False,
    placeholder='Select a month...'),

    html.Br(),
    html.Div(id="select-hour-div"),
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
    placeholder='Select an area...',
    id="select-area"),
  
    dcc.Checklist(id='select-all',                        #to add a select all tick box
    options=[{'label': 'Select all areas', 'value': 1}]),
    ]
    ),
    style={"width":"100%","height": "100%"})],width=4, #layout width are between 0 & 12
    align='center'), 

    
    dbc.Col([dbc.Button(dcc.Graph(id="graph_area_fig_pie",figure= blank_fig()),style={"width":"100%","height": "100%"})],width=4,
    align='center'),
    #to set up height of the component
    dbc.Col([dbc.Button(dcc.Graph(id="graph_day_name_area",figure= blank_fig()),style={"width": "100%","height": "100%"})],width=4),
    ], align='center'),
    html.Br(),
    dbc.Row([
    dbc.Col([dbc.Button(dcc.Graph(id="graph_per_hour_line",figure= blank_fig()), style={"width": "100%","height": "100%"})],width=6,
    align='center'),
    dbc.Col([dbc.Button(dcc.Graph(id="graph_per_hour_map",figure= blank_fig()),style={"width": "100%","height": "100%"})],width=6)
    ], align='center'),
]), color = 'dark'
    ),
        html.Br(),
    dbc.Row([
        dbc.Col([dbc.Button(html.Img(src=logo_dash, height="50px"),style={"width": "100%","height": "100%", "textAlign" :"left"})])

    ]) ])


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
    title='Repartition of crime type for selected area',)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label',#to put the label inside the pie
    hovertemplate="<br>".join(["Period: {} {}".format(month_choose,year_choose),
        "Hours range: between {}h and {}h".format(start_hour,end_hour),
        "Type of crime: %{label}",
        "Number: %{value}"] ))
    fig_pie.update_layout(legend_title_text= "Type of crime:",
    template='plotly_dark',
    paper_bgcolor='rgba(0, 0, 0, 0)', #to change the background color of the figure
    plot_bgcolor='rgba(0, 0, 0, 0)')#to change the background colour of the graph

    #to sort the df by day name in order, we give each day his ranking number ,we apply a lambda and add a new column
    df_area['day_ranking'] = df_area['day_name'].apply(lambda x: 0 if x == 'Monday'  
                                                                else 1 if x == 'Tuesday'
                                                                else 2 if x == 'Wednesday'
                                                                else 3 if x == 'Thursday'
                                                                else 4 if x == 'Friday'
                                                                else 5 if x =='Saturday'
                                                                else 6 if x =='Sunday'
                                                                else 'nothing')
                                                                
    df_area = df_area.reset_index(drop=True)
    df_line_day_name = df_area.groupby(['AREA NAME','day_name','day_ranking'])['Crm Cd Desc'].count().reset_index()
    df_line_day_name = pd.DataFrame(df_line_day_name)
    df_line_day_name = df_line_day_name.sort_values('day_ranking').reset_index(drop=True)

    fig_day_name_area = px.bar(df_line_day_name,x='day_name', y='Crm Cd Desc',color= 'AREA NAME',
    title="Sum of crime per day name and area")
    fig_day_name_area.update_traces(
        hovertemplate="<br>".join(["Day of the week: %{x}",
        "Number of crime: %{y}"] ))
    fig_day_name_area.update_layout(legend_title_text= "Area:",
    xaxis_title="{} {} between {}h and {}h".format(month_choose,year_choose,start_hour,end_hour),
    yaxis_title="Number of crime",
    template='plotly_dark',
    paper_bgcolor='rgba(0, 0, 0, 0)', #to change the background color of the figure
    plot_bgcolor='rgba(0, 0, 0, 0)')#to change the background colour of the graph
    fig_day_name_area.update_xaxes(showgrid = False)

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
    paper_bgcolor='rgba(0, 0, 0, 0)', #to change the background color of the figure
    plot_bgcolor='rgba(0, 0, 0, 0)')#to change the background colour of the graph
    fig_line.update_traces(
        hovertemplate="<br>".join([
    "Area: %{customdata[0]}",
    "Period: {} {}".format(month_choose,year_choose),
    "Hour: %{customdata[1]}",
    "Total crime number: %{customdata[2]}"
        ])
    )

    fig = px.scatter_mapbox(df_area, lat="LAT", lon="LON",color='AREA NAME',size= 'Vict Age',mapbox_style="open-street-map",
    title="LA's areas crime map for {} {} between {}h and {}h".format(month_choose, year_choose,start_hour,end_hour),
    custom_data=['AREA NAME','Vict Age','Vict Sex','Crm Cd Desc','TIME OCC','DATE OCC','LOCATION'],
    center={'lat': 34.052235, 'lon': -118.243683},#to center the map on LA
    zoom=7)
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
    paper_bgcolor='rgba(0, 0, 0, 0)', #to change the background color of the figure
    plot_bgcolor='rgba(0, 0, 0, 0)')#to change the background colour of the graph
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)


    return fig_pie, fig_day_name_area, fig_line, fig


if __name__ == "__main__":
    app.run_server(debug=False)
