import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
from math import pi

# Set the path that leads to the location of the folder, ending with the folder name
path = "C:\\Users\\User\\Desktop\\Radar Chart Demo"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Selecting Relevant Data: input user_id, modules, past data on input modules <br> <b> Aggregation: </b> adding vidPercentWatched, quizPercentCompleted <br> <b>Successful Student Average Values  </b>
def normalize(norm, username, inputModules):
    metricspastSuccessfulAggregatedDF = retSuccessfulStudent(inputModules)[0]
    metricscurrentAggregatedDF = retCurrStudent(username, inputModules)

    # Finding mean of past data
    metricspastSuccessfulAvgDF = retSuccessfulStudent(inputModules)[1]

    # Normalizing Factor
    if norm == 'all':
        normalizingFactor = pd.concat([metricscurrentAggregatedDF[displayCols], metricspastSuccessfulAggregatedDF[displayCols]]).max()
    elif norm == 'avg':
        normalizingFactor = pd.concat([metricscurrentAggregatedDF[displayCols], metricspastSuccessfulAvgDF[displayCols]]).max()

    # Normalizing
    metricscurrentNormalized = np.divide(np.array(metricscurrentAggregatedDF[displayCols]), np.array(normalizingFactor[displayCols])).flatten()
    metricspastSuccessfulNormalized = np.divide(np.array(metricspastSuccessfulAvgDF[displayCols]), np.array(normalizingFactor[displayCols])).flatten().tolist()
    return metricscurrentNormalized, metricspastSuccessfulNormalized

def retSuccessfulStudent(inputModules):
    modulesList = inputModules.split(',')
    modules = []
    for i, num in enumerate(modulesList):
        modules = modules + [int(num)]

    # past Data
    metricspastSuccessfulSelected = np.zeros((len(rawpast['user_id'].unique()), 9))
    for module in modules:
        adding = rawpast.loc[rawpast.module == str(module)].drop(nameCols, axis = 1)
        adding = np.array(adding)
        metricspastSuccessfulSelected += adding
    metricspastSuccessfulSelectedDF = pd.DataFrame(data = metricspastSuccessfulSelected, columns = rawCols)

    # past Data
    quizPercentCompletedpast = pd.DataFrame(data = metricspastSuccessfulSelectedDF['numQuizzesCompleted']/metricspastSuccessfulSelectedDF['numQuizzesAvailable'], columns = ['quizPercentCompleted'])
    vidPercentWatchedpast = pd.DataFrame(data = metricspastSuccessfulSelectedDF['numVidUniqueWatched']/metricspastSuccessfulSelectedDF['numVidUnique'], columns = ['vidPercentWatched'])
    avgTimelinesspast = pd.DataFrame(data = np.array(metricspastSuccessfulSelectedDF['quizTimeliness'])/np.array(metricspastSuccessfulSelectedDF['numQuizzesAvailable']), columns = ['avgTimeliness'])
    vidPercentRewatchedpast = pd.DataFrame(metricspastSuccessfulSelectedDF['numVidRewatches']/metricspastSuccessfulSelectedDF['numVidUnique'], columns = ['vidPercentRewatched'])
    avgResponsePerThreadpast = pd.DataFrame(metricspastSuccessfulSelectedDF['numUniquePosts']/metricspastSuccessfulSelectedDF['numUniqueThreads'], columns = ['avgResponsePerThread'])
    metricspastSuccessfulAggregatedDF = pd.concat([metricspastSuccessfulSelectedDF, quizPercentCompletedpast, vidPercentWatchedpast, avgTimelinesspast, vidPercentRewatchedpast, avgResponsePerThreadpast], axis = 1)

    # Finding mean of past data
    metricspastSuccessfulAvgDF = pd.DataFrame([metricspastSuccessfulAggregatedDF.mean()], columns = aggregatedCols)   

    return metricspastSuccessfulAggregatedDF, metricspastSuccessfulAvgDF

#returns current student with module values added together, plus aggregated values 
def retCurrStudent(username, inputModules):
    modulesList = inputModules.split(',')
    modules = []
    for i, num in enumerate(modulesList):
        modules = modules + [int(num)]

    # current Data
    metricscurrentStudent = rawcurrent.loc[rawcurrent.username == username]
    metricscurrentSelected = np.zeros((1, 9))
    for module in modules:
        adding = metricscurrentStudent.loc[metricscurrentStudent.module == str(module)].drop(nameCols, axis = 1)
        adding = np.array(adding)
        metricscurrentSelected += adding
    metricscurrentSelectedDF = pd.DataFrame(data = metricscurrentSelected, columns = rawCols)

    # Add aggregated values
    # current Data
    quizPercentCompletedcurrent = pd.DataFrame(data = metricscurrentSelectedDF['numQuizzesCompleted']/metricscurrentSelectedDF['numQuizzesAvailable'], columns = ['quizPercentCompleted'])
    vidPercentWatchedcurrent = pd.DataFrame(data = metricscurrentSelectedDF['numVidUniqueWatched']/metricscurrentSelectedDF['numVidUnique'], columns = ['vidPercentWatched'])
    avgTimelinesscurrent = pd.DataFrame(data = np.array(metricscurrentSelectedDF['quizTimeliness'])/np.array(metricscurrentSelectedDF['numQuizzesAvailable']), columns = ['avgTimeliness'])
    vidPercentRewatchedcurrent = pd.DataFrame(metricscurrentSelectedDF['numVidRewatches']/metricscurrentSelectedDF['numVidUnique'], columns = ['vidPercentRewatched'])
    avgResponsePerThreadcurrent = pd.DataFrame(metricscurrentSelectedDF['numUniquePosts']/metricscurrentSelectedDF['numUniqueThreads'], columns = ['avgResponsePerThread'])

    metricscurrentAggregatedDF = pd.concat([metricscurrentSelectedDF, quizPercentCompletedcurrent, vidPercentWatchedcurrent, avgTimelinesscurrent, vidPercentRewatchedcurrent, avgResponsePerThreadcurrent], axis = 1)
    return metricscurrentAggregatedDF

#import student info, quiz and video metrics 
#Note: here, past student data contain only those who have completed the course
past_QV = pd.read_excel(path + "\\CSVs\\Video Quizzes Info\\past_QV.xlsx")
current_QV = pd.read_excel(path + "\\CSVs\\Video Quizzes Info\\current_QV.xlsx")

#import written discussion info
#Note: here, past student data contain all student data, same for all discussion data
past_D = pd.read_excel(path + "\\CSVs\\Discussion Posts\\past_D.xlsx")
current_D = pd.read_excel(path + "\\CSVs\\Discussion Posts\\current_D.xlsx")

#import view discussion info
past_DV = pd.read_excel(path + "\\CSVs\\Discussion Views\\past_DV.xlsx")
current_DV = pd.read_excel(path + "\\CSVs\\Discussion Views\\current_DV.xlsx")

#import discussion post/module mapping 
past_DM = pd.read_excel(path + "\\CSVs\\Discussion Mapping\\past_DM.xlsx")
current_DM = pd.read_excel(path + "\\CSVs\\Discussion Mapping\\current_DM.xlsx")

#Missing Value Treatment for Discussion Data
#written discussion info missing value treatment
past_D['thread_id'].fillna(past_D['slug_id'], inplace = True)
current_D['thread_id'].fillna(current_D['slug_id'], inplace = True)

#view discussion info missing value treatment
past_DV.dropna(subset = ['username'], axis = 0, inplace = True)
current_DV.dropna(subset = ['username'], axis = 0, inplace = True)

#discussion post/module mapping missing value treatment
past_DM.dropna(subset = ['module'], axis = 0, inplace = True)
current_DM.dropna(subset = ['module'], axis = 0, inplace = True)


#Merging discussion data
#Merging discussion posts and mapping dataframes
discussion_modulepast = pd.merge(past_D, past_DM[['slug_id', 'module']], on = 'slug_id', how = 'left')
discussion_modulecurrent = pd.merge(current_D, current_DM[['slug_id', 'module']], on = 'slug_id', how = 'left')

#Check missing values
#Note: if there are any null values in module, then slug_id entries are errorneous or post/module mappings are incomplete
#Note: if so, drop rows with null module information in the next line, may need to updat mapping information
#Note: there should not be any null values other than in module
discussion_modulepast.dropna(subset = ['module'], axis = 0, inplace = True)
discussion_modulecurrent.dropna(subset = ['module'], axis = 0, inplace = True)

#Merging discussion post views and mapping dataframes
discView_modulepast = pd.merge(past_DV, past_DM[['slug_id', 'module']], left_on = 'thread_id', right_on = 'slug_id', how = 'left')
discView_modulepast.drop('slug_id', axis = 1, inplace = True)
discView_modulecurrent = pd.merge(current_DV, current_DM[['slug_id', 'module']], left_on = 'thread_id', right_on = 'slug_id', how = 'left')
discView_modulecurrent.drop('slug_id', axis = 1, inplace = True)

#Check missing values
#Note: if there are any null values here, then slug_id entries are errorneous or post/module mappings are incomplete
#Note: if so, drop rows with null module information in the next line
discView_modulepast.dropna(subset = ['module'], axis = 0, inplace = True)
discView_modulecurrent.dropna(subset = ['module'], axis = 0, inplace = True)

#Aggregating discussion data
#Aggregating number of post viewed per module
discView_aggpast = discView_modulepast.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).count()
discView_aggpast.rename(columns = {'thread_id':'numPostViewed'}, inplace = True)
discView_aggcurrent = discView_modulecurrent.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).count()
discView_aggcurrent.rename(columns = {'thread_id':'numPostViewed'}, inplace = True)

#Aggregating number of posts, number of threads per module
discussion_aggpastS = discussion_modulepast.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).agg({'slug_id': pd.Series.nunique})
discussion_aggpastS.rename(columns = {'slug_id':'numUniquePosts'}, inplace = True)
discussion_aggpastT = discussion_modulepast.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).agg({'thread_id': pd.Series.nunique})
discussion_aggpastT.rename(columns = {'thread_id':'numUniqueThreads'}, inplace = True)

discussion_aggcurrentS = discussion_modulecurrent.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).agg({'slug_id': pd.Series.nunique})
discussion_aggcurrentS.rename(columns = {'slug_id':'numUniquePosts'}, inplace = True)
discussion_aggcurrentT = discussion_modulecurrent.groupby(['course_id', 'username', 'module'], axis = 0, as_index = False).agg({'thread_id': pd.Series.nunique})
discussion_aggcurrentT.rename(columns = {'thread_id':'numUniqueThreads'}, inplace = True)

discussion_aggpast = pd.merge(discussion_aggpastT, discussion_aggpastS, on = ['course_id', 'username', 'module'])
discussion_aggcurrent = pd.merge(discussion_aggcurrentT, discussion_aggcurrentS, on = ['course_id', 'username', 'module'])

#Merging all discussion data
discussion_aggAllpast = pd.merge(discView_aggpast, discussion_aggpast, on = ['course_id', 'username', 'module'], how = 'outer')
discussion_aggAllcurrent = pd.merge(discView_aggcurrent, discussion_aggcurrent, on = ['course_id', 'username', 'module'], how = 'outer')

#Checking for missing values
discussion_aggAllpast[['numPostViewed', 'numUniqueThreads', 'numUniquePosts']] = discussion_aggAllpast[['numPostViewed', 'numUniqueThreads', 'numUniquePosts']].fillna(0)
discussion_aggAllcurrent[['numPostViewed', 'numUniqueThreads', 'numUniquePosts']] = discussion_aggAllcurrent[['numPostViewed', 'numUniqueThreads', 'numUniquePosts']].fillna(0)

#Check if numPostViewed < numUniquePosts (posts written), if so, definition of data may be wrong, or individual entries may be errorneous (10/239 in current, 27/1037 in past)
discussion_aggAllpast['que'] = np.where(discussion_aggAllpast['numPostViewed'] >= discussion_aggAllpast['numUniquePosts'], True, False)
discussion_aggAllcurrent['que'] = np.where(discussion_aggAllcurrent['numPostViewed'] >= discussion_aggAllcurrent['numUniquePosts'], True, False)

# Set the column numPostViewed for rows where numPostViewed < numUniquePosts to be the value in column numUniquePosts
discussion_aggAllpast.loc[discussion_aggAllpast['que'] == False, 'numPostViewed'] = discussion_aggAllpast.loc[discussion_aggAllpast['que'] == False, 'numUniquePosts']
discussion_aggAllcurrent.loc[discussion_aggAllcurrent['que'] == False, 'numPostViewed'] = discussion_aggAllcurrent.loc[discussion_aggAllcurrent['que'] == False, 'numUniquePosts']

#Missing Value Treatment for student_quiz_video info, Data Formatting
# Missing Value Treatment
past_QV["numQuizzesCompleted"].fillna(0, inplace=True)
current_QV["numQuizzesCompleted"].fillna(0, inplace=True)
past_QV["quizTimeliness"].fillna(0, inplace=True)
current_QV["quizTimeliness"].fillna(0, inplace=True)

past_QV['numVidRewatches'].fillna(past_QV['numVidRewatches'].mode().iloc[0], inplace=True)
current_QV['numVidRewatches'].fillna(current_QV['numVidRewatches'].mode().iloc[0], inplace=True)
past_QV['numVidUniqueWatched'].fillna(past_QV['numVidUniqueWatched'].mode().iloc[0], inplace=True)
current_QV['numVidUniqueWatched'].fillna(current_QV['numVidUniqueWatched'].mode().iloc[0], inplace=True)

past_QV[['numQuizzesCompleted', 'numVidRewatches', 'numVidUniqueWatched']] = past_QV[['numQuizzesCompleted', 'numVidRewatches', 'numVidUniqueWatched']].astype('int64')
current_QV[['numQuizzesCompleted', 'numVidRewatches', 'numVidUniqueWatched']] = current_QV[['numQuizzesCompleted', 'numVidRewatches', 'numVidUniqueWatched']].astype('int64')
past_QV[['course_id', 'module', 'username', 'user_id']] = past_QV[['course_id', 'module', 'username', 'user_id']].astype('str')
current_QV[['course_id', 'module', 'username', 'user_id']] = current_QV[['course_id', 'module', 'username', 'user_id']].astype('str')

discussion_aggAllpast[['course_id', 'module', 'username']] = discussion_aggAllpast[['course_id', 'module', 'username']].astype('str')
discussion_aggAllcurrent[['course_id', 'module', 'username']] = discussion_aggAllcurrent[['course_id', 'module', 'username']].astype('str')

discussion_aggAllpast.drop(index = discussion_aggAllpast[discussion_aggAllpast['module']=='Course'].index, inplace = True)
discussion_aggAllcurrent.drop(index = discussion_aggAllcurrent[discussion_aggAllcurrent['module']=='Course'].index, inplace = True)
discussion_aggAllpast.drop(columns = ['que'], inplace=True)
discussion_aggAllcurrent.drop(columns = ['que'], inplace=True)

#left join to select successful students
rawpast = pd.merge(past_QV, discussion_aggAllpast, on = ['course_id', 'username', 'module'], how = 'left')

rawpast['numPostViewed'].fillna(rawpast['numPostViewed'].mode().iloc[0], inplace=True)
rawpast['numUniqueThreads'].fillna(rawpast['numUniqueThreads'].mode().iloc[0], inplace=True)
rawpast['numUniquePosts'].fillna(rawpast['numUniquePosts'].mode().iloc[0], inplace=True)

#left join since current_QV contains all registered students
rawcurrent = pd.merge(current_QV, discussion_aggAllcurrent, on = ['course_id', 'username', 'module'], how = 'left')
rawcurrent['numPostViewed'].fillna(rawcurrent['numPostViewed'].mode().iloc[0], inplace=True)
rawcurrent['numUniqueThreads'].fillna(rawcurrent['numUniqueThreads'].mode().iloc[0], inplace=True)
rawcurrent['numUniquePosts'].fillna(rawcurrent['numUniquePosts'].mode().iloc[0], inplace=True)

rawCols = ['numQuizzesAvailable', 'numQuizzesCompleted', 'quizTimeliness', 'numVidRewatches', 'numVidUniqueWatched', 'numVidUnique', 'numUniqueThreads', 'numUniquePosts', 'numPostViewed']
nameCols = ['course_id', 'user_id', 'username', 'module']
rawpast = rawpast[nameCols + rawCols]
rawcurrent = rawcurrent[nameCols + rawCols]

#Exporting Data
rawpast.to_csv(path + '\\CSVs\\Python Outfiles (raw)\\rawpast.csv')
rawcurrent.to_csv(path + '\\CSVs\\Python Outfiles (raw)\\rawcurrent.csv')
aggregatedCols = rawCols + ['quizPercentCompleted', 'vidPercentWatched', 'avgTimeliness', 'vidPercentRewatched', 'avgResponsePerThread']
displayCols = ['numUniqueThreads', 'numPostViewed', 'quizPercentCompleted', 'avgTimeliness', 'vidPercentRewatched', 'vidPercentWatched', 'avgResponsePerThread']

#Adding example student for demonstration purposes
#rawcurrent.loc[len(rawcurrent)] = ['UBCx/China200.1x/1Tcurrent', '0000000', 'example_student', '1', 1, 1, 121.0, 2, 11, 13, 3, 3, 5]
#rawcurrent.loc[len(rawcurrent)+1] = ['UBCx/China200.1x/1Tcurrent', '0000000', 'example_student', '2', 1, 1, 31.0, 3, 11, 12, 2, 2, 2]
#rawcurrent.loc[len(rawcurrent)+2] = ['UBCx/China200.1x/1Tcurrent', '0000000', 'example_student', '3', 1, 1, 5.0, 1, 13, 12, 1, 2, 4]
#rawcurrent.loc[len(rawcurrent)+3] = ['UBCx/China200.1x/1Tcurrent', '0000000', 'example_student', '4', 1, 0, 0.0, 1, 7, 13, 0, 0, 3]

app.layout = html.Div(children=[
    html.H1(
        children='Student Progress Dashboard',
        style={
            'textAlign': 'center',
    }),

    html.H6(
        children='Course ID: ' + str(current_QV['course_id'].unique()),
        style={
            'textAlign': 'center',
    }),

    html.Br(),

    html.Div(className = 'row', children=[
        html.Div(className = 'column', children=[''' ''']),   
        html.Div(className = 'two columns', children=['''Enter your username:''', dcc.Input(id='student_id_in', value = 'e.g. "example_student"', type= 'text')]),   
        html.Div(className = 'three columns', children=['''Choose modules (separated by commas):''', dcc.Input(id='modules_in', value = 'eg. "1, 2, 4"', type= 'text')]), 
        html.Div(className = 'four columns', children=[
            '''Choose a normalization option: ''',
            dcc.RadioItems(
                #className = 'four columns',
                id = 'normalization',
                options=[
                    {'label': 'By maximum of current, and average of successful students', 'value': 'avg'},
                    {'label': 'By maximum of current, and all successful students', 'value': 'all'}
                ],
                value='avg'
            )
        ]), 
        html.Div(className = 'two columns', children=[html.Button(id='button_refreshGraph', n_clicks=0, children='Refresh')])
    ]),

    html.Br(),

    html.Div(className = 'row', children=[
        html.Div(className = 'six columns', children=[
            dcc.Graph(
                id='radar_chart',
                figure = {
                        'data' : [go.Scatterpolar(
                            r=[0, 0, 0, 0, 0, 0, 0],
                            theta = ['Breadth of Discussion Posts', 'Viewed Discussion Posts', 'Fraction of Quizzes Completed', 'Timeliness of Quiz Completion', 'Fraction of Videos Rewatched', 'Fraction of Videos Watched', 'Depth of Discussion Posts'],
                            fill='toself',
                            line_color = 'orange'
                        )],
                        'layout' : go.Layout(
                            title = "Your Progress",
                            margin=dict(l=120, r=100, t=140, b=80),
                            polar = dict(radialaxis = dict(visible=False), angularaxis = dict(rotation=90, direction="clockwise"))
                        )
                }
            )
        ]),
        html.Div(id = 'bar_chart', className = 'five columns', children=[
            dcc.Graph(
                figure = {
                    'data' : [go.Bar(
                        x = [0, 0],
                        y = ['Successful Student', 'Current Student'],
                        orientation = 'h')
                    ],
                    'layout' : go.Layout(
                        width = 700,
                        height = 300,
                        title = 'Details',
                        margin=dict(l=120, r=100, t=140, b=80)
                    )                    
                }
            ),
            html.Div(children ='Click on orange data points to see details.')      
        ])
    ])
])

@app.callback(
    Output(component_id='radar_chart', component_property='figure'),
    [Input(component_id='button_refreshGraph', component_property = 'n_clicks')],
    [State(component_id='normalization', component_property='value'),
    State(component_id='student_id_in', component_property='value'),
    State(component_id='modules_in', component_property='value')]
)
def update_graph(n_clicks, norm, sid_in, m_in):
    return {
        'data' : [
                go.Scatterpolar(
                    r = normalize(norm, sid_in, str(m_in))[1],
                    theta = ['Breadth of Discussion Posts', 'Viewed Discussion Posts', 'Fraction of Quizzes Completed', 'Timeliness of Quiz Completion', 'Fraction of Videos Rewatched', 'Fraction of Videos Watched', 'Depth of Discussion Posts'],
                    #displayCols = ['numUniqueThreads', 'numPostViewed', 'quizPercentCompleted', 'avgTimeliness', 'vidPercentRewatched', 'vidPercentWatched', 'avgResponsePerThread']
                    fill='toself',
                    line_color='blue',
                    name = 'Successful Student'),
                go.Scatterpolar(
                    r = normalize(norm, sid_in, str(m_in))[0],
                    theta = ['Breadth of Discussion Posts', 'Viewed Discussion Posts', 'Fraction of Quizzes Completed', 'Timeliness of Quiz Completion', 'Fraction of Videos Rewatched', 'Fraction of Videos Watched', 'Depth of Discussion Posts'],
                    fill='toself',
                    line_color='orange',
                    name = 'Current Student',
                    hovertext=["Click to see participated discussion threads.", "Click to see your viewed posts.", "Click to see completed quizzes.", "Click to see timeliness of quiz completion.",\
                                "Click to see re-watched videos.", "Click to see watched videos.", "Click to see your posts."],
                    hoverinfo = 'text')
        ],
        'layout' : go.Layout(
                    title = sid_in + "'s Progress",
                    polar = dict(radialaxis = dict(visible=False), angularaxis = dict(rotation=90, direction="clockwise")),
                    yaxis=dict(
                        autorange=True,
                        automargin=True
                    ),
                    margin=dict(l=120, r=100),
                    legend=dict(x=1, y=1.1)
        )
    }

@app.callback(
    Output(component_id='bar_chart', component_property='children'),
    [Input(component_id='radar_chart', component_property='clickData'),
    Input(component_id='button_refreshGraph', component_property = 'n_clicks')],
    [State(component_id='student_id_in', component_property='value'),
    State(component_id='modules_in', component_property='value')]
)
def display_click_data(clickData, buttonpress, sid, modules):
    theta1 = clickData["points"][0]["theta"]  
    currStudent = retCurrStudent(sid, modules)
    succStudent = retSuccessfulStudent(modules)[1]

    if theta1 == 'Breadth of Discussion Posts':
        theta = 'numUniqueThreads'
        inputText = 'written post(s) in a total of ' + "{:.0f}".format(currStudent.at[0, theta]) + ' threads(s)'
        inputText2 = 'written post(s) in a total of ' + "{:.0f}".format(succStudent.at[0, theta]) + ' threads(s)'
    elif theta1 == 'Viewed Discussion Posts':
        theta = 'numPostViewed'
        inputText = 'viewed a total of ' + "{:.0f}".format(currStudent.at[0, theta]) + ' post(s)'
        inputText2 = 'viewed a total of ' + "{:.0f}".format(succStudent.at[0, theta]) + ' post(s)'
    elif theta1 == 'Fraction of Quizzes Completed':
        theta = 'quizPercentCompleted'
        inputText = 'completed a total of ' + "{:.0f}".format(currStudent.at[0, 'numQuizzesCompleted']) + r'/' + "{:.0f}".format(currStudent.at[0, 'numQuizzesAvailable']) + ' quiz(zes)'
        inputText2 = 'completed a total of ' + "{:.0f}".format(succStudent.at[0, 'numQuizzesCompleted']) + r'/' + "{:.0f}".format(succStudent.at[0, 'numQuizzesAvailable']) + ' quiz(zes)'       
    elif theta1 == 'Timeliness of Quiz Completion':
        theta = 'avgTimeliness'
        inputText = 'finished, on average, each quiz ' + "{:.0f}".format(currStudent.at[0, theta]) + ' hour(s) before the deadline'
        inputText2 = 'finished, on average, each quiz ' + "{:.0f}".format(succStudent.at[0, theta]) + ' hours(s) before the deadline'
    elif theta1 == 'Fraction of Videos Rewatched':
        theta = 'vidPercentRewatched'
        inputText = 'rewatched a total of ' + "{:.0f}".format(currStudent.at[0, 'numVidRewatches']) + r'/' + "{:.0f}".format(currStudent.at[0, 'numVidUnique']) + ' video(s)'
        inputText2 = 'rewatched a total of ' + "{:.0f}".format(succStudent.at[0, 'numVidRewatches']) + r'/' + "{:.0f}".format(succStudent.at[0, 'numVidUnique']) + ' video(s)'       
    elif theta1 == 'Fraction of Videos Watched':
        theta = 'vidPercentWatched'
        inputText = 'watched a total of ' + "{:.0f}".format(currStudent.at[0, 'numVidUniqueWatched']) + r'/' + "{:.0f}".format(currStudent.at[0, 'numVidUnique']) + ' video(s)'
        inputText2 = 'watched a total of ' + "{:.0f}".format(succStudent.at[0, 'numVidUniqueWatched']) + r'/' + "{:.0f}".format(succStudent.at[0, 'numVidUnique']) + ' video(s)'  
    elif theta1 == 'Depth of Discussion Posts':
        theta = 'avgResponsePerThread'
        inputText = 'written ' + "{:.0f}".format(currStudent.at[0, theta]) + ' post(s) per thread participated in'
        inputText2 = 'written ' + "{:.0f}".format(succStudent.at[0, theta]) + ' post(s) per thread participated in'

    return [
        dcc.Graph(
            figure={
                'data' : [go.Bar(
                        x = [succStudent.at[0, theta], currStudent.at[0, theta]],
                        y = ['Successful Student', sid],
                        orientation = 'h',
                        marker_color = ['blue', 'orange'])
                ],
                'layout' : go.Layout(
                    width = 700,
                    height = 300,
                    title = theta1,
                    margin = dict(l=120, r=100)
                ) 
            }
        ),
        html.Div(children ='In module(s) ' + modules + ', you have ' + inputText + ', while an average passing student has ' + inputText2 + '.')      
    ]

PORT = 2000
if __name__ == '__main__':
    app.run_server(port = PORT)