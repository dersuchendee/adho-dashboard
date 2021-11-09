import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import io
import requests

pio.templates.default = "ggplot2"
app.title = 'ADHO Social Media Dashboard'
#####################################
# Add your data
#####################################

#example iris dataset
#df = px.data.iris()

#most_liked = pd.read_csv('most_liked.csv')
#most_replied = pd.read_csv('most_replied.csv')
#most_retweeted = pd.read_csv('most_retweeted.csv')
most_used_hashtags = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/popular_hashtags.csv') #done
#best_hours = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/Twitter/main/best_hours.csv') #done
best_hours = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/hours_stats.csv')
activity_timeline = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/activity_07080910_2021.csv') #done
week_stats = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/week_mean.csv')
week_impressions = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/week_impressions.csv')
engagement = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/engagement.csv')
most_mentioned=pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/most_mentioned.csv')
most_retweeted=pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/most_retweeted.csv')
correlations = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/correlations.csv')
facebook1 =  pd.read_csv(io.StringIO("""Paesi_principali,Value,iso_alpha
Stati Uniti,16.6,US
Italia,10.6,IT
Germania,5,DE
Messico,4.6,MX
India,4.2,IN
Francia,3.7,FR
Regno Unito,3.7,UK
Spagna,3.3,ES
Canada,3.1,CA
Grecia,3.1,GR"""))

#facebook2 = pd.read_csv('https://raw.githubusercontent.com/dersuchendee/adho-dashboard/main/Facebook_likes_gender_age.csv')

#####################################
# Styles & Colors
#####################################

NAVBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "top":0,
    "margin-top":'2rem',
    "margin-left": "18rem",
    "margin-right": "2rem",
}

#####################################
# Create Auxiliary Components Here
#####################################

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
    [
        html.H4("ADHO Social Media Performance Dashboard", className="display-10",style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Twitter", href="/page1",active="exact", external_link=True),
                dbc.NavLink("Facebook", href="/page2", active="exact", external_link=True)
            ],
            pills=True,
            vertical=True
        ),
    ],
    style=NAVBAR_STYLE,
    )
    
    return navbar

#graph 1
example_graph1 = px.bar(activity_timeline, x="month",y="counts",

                 labels={
                     "month": "Month",
                     "counts": "Number of tweets"
                 },
                         title='Twitter activity') #activity over time

example_graph1.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

#graph 2
most_used_hashtags = most_used_hashtags.head(10)
example_graph2 = px.bar(most_used_hashtags, x="hashtag", y="counts",
                        labels={
                            "hashtag": "Hashtag",
                            "counts": "Number"
                        }, title = 'Most used hashtags')

#graph3
example_graph3 = px.line(best_hours, x='hour', y=['engagements', 'retweets','likes'],
labels = {
             "hour": "Hour",
            'engagements': 'Engagements',
    'retweets': 'Retweets',
    'likes' : 'Likes'

         },
         title = 'Best hours for tweeting'
)
example_graph3.update_xaxes(type='category')
    #px.bar(best_hours, x="time", y="likes_count"
     #                   ,
      #                  labels={
       #                     "time": "Hour of the day",
        #                    "likes_count": "Number of likes"
         #               },
          #              title='Best hours for tweeting')

#graph4
example_graph4 = px.line(week_stats, x='day_name', y=['engagements', 'retweets','likes'],
labels = {
             "day_name": "Day",
'engagements': 'Engagements',
    'retweets': 'Retweets',
    'likes' : 'Likes'

         },
         title = 'Week stats'
)
#graph5
s = week_impressions['count']/week_impressions['mean']
week_impressions['ratio'] = s
example_graph5 = px.bar(week_impressions, x='day_name', y=['count', 'mean'], barmode='group',
labels = {"day_name": "Day",
          'count':'Number of tweets',
'mean ':'Mean impressions'


},
          title = 'Number of tweets vs mean of impressions by day of the week')
#graph6
m = max(engagement['engagement_rate'])
# Number of data points: n
n = len(engagement['engagement_rate'])
    # x-data for the ECDF: x
xe = np.sort(engagement['engagement_rate'])
    # y-data for the ECDF: y
ye = np.arange(1, n+1) / n
mean = engagement['engagement_rate'].mean()
std = engagement['engagement_rate'].std()
samples = np.random.normal(mean, std, 1000)
#theoretical data
n_theor = len(samples)
    # x-data for the ECDF: x
x_theor = np.sort(samples)
    # y-data for the ECDF: y
y_theor = np.arange(1, n_theor+1) / n_theor
import plotly.graph_objects as go
example_graph6 = go.Figure()
example_graph6.add_trace(go.Scatter(x=x_theor, y=y_theor, name='Normal distribution',
                         line=dict(color='royalblue', width=4, dash='dot')))
example_graph6.add_trace(go.Scatter(x=xe, y=ye, name='Empirical data',
                         line=dict(color='firebrick', width=4,
                              dash='dot'))), # dash options include 'dash', 'dot', and 'dashdot'
example_graph6.update_layout(title='Engagement rate',
                   xaxis_title='Engagement',
                   yaxis_title='eCDF')
#graph7
most_mentioned= most_mentioned.head(10)
example_graph7 = px.bar(most_mentioned, x='word', y='count',
                        labels = {
                            'word':'Handle',
                            'count': 'Count'
                        }, title = 'Most mentioned')
#graph8
most_retweeted= most_retweeted.head(10)
example_graph8 = px.bar(most_retweeted, x='quote_url', y='count',
                        labels = {
                            'quote_url':'Handle',
                            'count': 'Count'
                        }, title = 'Most retweeted')
#graph9
example_graph9 = px.imshow(correlations)
labels=dict(x=['impressions','engagements','engagement_rate','retweets','replies','likes','profile_clicks','url_clicks','day'],
     y=['impressions','engagements','engagement_rate','retweets','replies','likes','profile_clicks','url_clicks','day'])
example_graph9.update_xaxes(side="top")

#graph10
# get iso_code 3 chars for countries
dfloc = pd.read_html(
    "https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/locations.csv"
)[0]

# join and fix 2 character codes to 3 character codes
facebook1 = facebook1.merge(
    dfloc.assign(iso2=np.where(dfloc["iso_code"].eq("GBR"), "UK",dfloc["iso_code"].str[0:2])).loc[
        :, ["iso_code", "location", "iso2"]
    ],
    left_on="iso_alpha",
    right_on="iso2",
    how="inner",
).pipe(lambda d: d.loc[~d["iso_code"].isin(["EST","FRO","GRL","GRD","CAF"])])

example_graph10 =   px.scatter_geo(facebook1, locations="iso_code",locationmode ="ISO-3", color="iso_code",
                         hover_name="iso_code", size="Value",
                         projection="natural earth", title="Facebook fans by country (values in percentage)", labels=
                                   {
                                       'Paesi_principali':'Countries',
                                       'iso_code':'Country'
                                   })

#graph11
import plotly.graph_objs as go
import plotly.graph_objects as go
interval=["18-24", "25-34", "35-44","45-54", "55-64","65+"]
Men = [2,13.7,14.6,8,2.9,1.6]
Women = [1.8, 20.9, 19.3, 9.3,3.6,2.3]

example_graph11 = go.Figure( data=[
    go.Bar(name='Women', x=interval, y=Women),
    go.Bar(name='Men', x=interval, y=Men)
])
# Change the bar mode
example_graph11.update_layout(barmode='group', title = "Facebook fans by age and gender*")



#####################################
# Create Page Layouts Here
#####################################


### Layout 1
layout1 = html.Div([
    html.H2("Twitter analytics"),
    html.Hr(),
#dbc.CardGroup(
   # [
    #    dbc.Card(
    #        dbc.CardBody(
    #           [
    ##               html.H5("9,542 Followers", className="card-title"),
    #              html.P(
    #                   "Twitter",
    #                   className="card-text",
    #               )
#
    ###               ]
#
    #           )
    ###   ),
    # dbc.Card(
    #       dbc.CardBody(
    #           [
    #               html.H5("2,518 Likes", className="card-title"),
    #               html.P(
    #                   "Facebook",
    #                   className="card-text",
    #               )
#
    #               ]
    #       )
    #   ),
    #   dbc.Card(
    #       dbc.CardBody(
    #           [
    #               html.H5("Card 3", className="card-title"),
    #               html.P(
    ###                   "This card has some text content, which is longer "
    #                 ,
    #                   className="card-text",
    #               ),
#
    #               ],
#style={"height": "30px"},
    #           )
    #   ),
    #],



#),

    # create bootstrap grid
    dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                            #html.H4('General'),

                            #create tabs
                            dbc.Tabs(
                                [
                                    dbc.Tab(label='Activity',tab_id='graph1'),
dbc.Tab(label='Best hours',tab_id='graph3'),
dbc.Tab(label='Week stats',tab_id='graph4'),
dbc.Tab(label='Impressions',tab_id='graph5'),
dbc.Tab(label='Engagement',tab_id='graph6'),
dbc.Tab(label="Correlations", tab_id='graph9')
                                ],
                                id="tabs",
                                active_tab='graph1',
                                ),
                            html.Div(id="tab-content",className="p-4")
                            ]
                        ),
                    ], style={'marginBottom': 5, 'marginTop': 15},
                    width=12 #half page,


                ),

                
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div([
                           dcc.Graph(
                                id='graph-2',
                                figure=example_graph2
                            )]),


                    ], style={'marginBottom': 10, 'marginTop': 5},
                    width=4

                ),
dbc.Col(
                    [
                        html.Div([
                           dcc.Graph(
                                id='graph-8',
                                figure=example_graph8
                            )]),


                    ], style={'marginBottom': 10, 'marginTop': 5},
                    width=4  # half page,

                ),
dbc.Col(
                    [
                        html.Div([
                           dcc.Graph(
                                id='graph-7',
                                figure=example_graph7
                            )]),


                    ], style={'marginBottom': 10, 'marginTop': 5},
                    width=4  # half page,

                ),

            ],
        ),
    ]),
])


### Layout 2

layout2 = html.Div(
    [
        html.H2('Facebook analytics'),
        html.Hr(),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
html.Div([
                           dcc.Graph(
                                id='graph-10',
                                figure=example_graph10
                            )
]),

                            ],

                        )
                    ]
                ),
dbc.Row(
                    [
                        dbc.Col(
                            [
html.Div([
                            dcc.Graph(
                                id='graph-11',
                                figure=example_graph11
                            ),
    html.P('*Data downloaded by Facebook. Data lastly updated in September, 2021')
]),

                            ],

                        )
                    ]
                ),
            ]

        )
    ])