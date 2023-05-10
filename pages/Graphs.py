
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from dash import html, dcc, callback, Input, Output
import plotly.figure_factory as ff

dash.register_page(__name__)

pd.set_option("display.max_rows", None, "display.max_columns", None)

data=pd.read_csv('h1b18.csv')
data.dropna(inplace=True)


# removing data which is not necessary
data['CASE_SUBMITTED']=pd.to_datetime(data['CASE_SUBMITTED'])
data['month_CASE_SUBMITTED'] = pd.DatetimeIndex(data['CASE_SUBMITTED']).month


data['DECISION_DATE']=pd.to_datetime(data['DECISION_DATE'])
data['month_Decision'] = pd.DatetimeIndex(data['DECISION_DATE']).month

data['EMPLOYMENT_START_DATE']=pd.to_datetime(data['EMPLOYMENT_START_DATE'])
data['EMPLOYMENT_END_DATE']=pd.to_datetime(data['EMPLOYMENT_END_DATE'])

data['month_EMPLOYMENT_START'] = pd.DatetimeIndex(data['EMPLOYMENT_START_DATE']).month
data['month_EMPLOYMENT_End'] = pd.DatetimeIndex(data['EMPLOYMENT_END_DATE']).month


data["PREVAILING_WAGE"]=data["PREVAILING_WAGE"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_FROM"]=data["WAGE_RATE_OF_PAY_FROM"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_TO"]=data["WAGE_RATE_OF_PAY_TO"].str.replace(",", "").astype(float)


data=data.drop(['SOC_CODE', 'SOC_NAME','CASE_NUMBER','EMPLOYER_POSTAL_CODE','EMPLOYER_CITY','WAGE_RATE_OF_PAY_TO','WAGE_UNIT_OF_PAY'], axis=1)
data.dropna(inplace = True)
print(data.head())
data=data.head(50000)
print(data.nunique().sort_values(ascending=True))
print(data.shape)


df_heatmap = data.groupby('EMPLOYER_STATE')['CASE_STATUS'].count()
print(df_heatmap)
accept_arr = data['CASE_STATUS'].value_counts()
print(accept_arr)
accept_val = list(accept_arr)[0:4]
accept_label = list(accept_arr.index)[0:4]

graphs=["Histogram","Scatterplot","Pie Chart","Line chart","count plot", "heat map","Bar plot",
        "Pair plot","Box plot","Regression plot"]
list=['None','CASE_STATUS','month_CASE_SUBMITTED','month_Decision','EMPLOYMENT_END_DATE','month_EMPLOYMENT_End' ,'CASE_SUBMITTED', 'DECISION_DATE', 'VISA_CLASS',
       'EMPLOYMENT_START_DATE', 'EMPLOYER_NAME',
       'EMPLOYER_STATE', 'JOB_TITLE', 'FULL_TIME_POSITION', 'PREVAILING_WAGE',
       'PW_UNIT_OF_PAY', 'WAGE_RATE_OF_PAY_FROM']
list2=['CASE_STATUS','month_CASE_SUBMITTED','month_Decision','EMPLOYMENT_END_DATE','month_EMPLOYMENT_End' ,'CASE_SUBMITTED', 'DECISION_DATE', 'VISA_CLASS',
       'EMPLOYMENT_START_DATE', 'EMPLOYER_NAME',
       'EMPLOYER_STATE', 'JOB_TITLE', 'FULL_TIME_POSITION', 'PREVAILING_WAGE',
       'PW_UNIT_OF_PAY', 'WAGE_RATE_OF_PAY_FROM']

layout = html.Div([
    dbc.Row(
            [
                html.Div(
                    [
                        html.H1('Pick a feature'),
                        html.Br(),
                        html.P("X axis"),
                        dcc.Checklist(options=list,
                                     id='col_na',value=['VISA_CLASS'], inline= False,
                                      labelStyle={'display': 'block'},
                                      style={"height":200, "width":200, "overflow":"auto"}),
                    ],
                )]),
    dbc.Row(
        [
            html.Div(
                [
                    html.H1('Pick a feature'),
                    html.Br(),
                    html.P("Y axis"),
                    dcc.RadioItems(options=list,
                                  id='col_na2', inline=False,
                                  labelStyle={'display': 'block'},
                                style={"height":200, "width":500, "overflow":"auto"}),
                ],
            )]),
    html.Br(),
    dbc.Row(
        [
            html.Div(
                [
                    html.H1('Pick a feature'),
                    html.Br(),
                    html.P("Hue (Optional)"),
                    dcc.RadioItems(options=list,
                                   id='col_na3', inline=False,
                                   labelStyle={'display': 'block'},
                                   style={"height": 200, "width": 500, "overflow": "auto"}),
                ],
            )]),
    html.Br(),
    dbc.Row(
        [
            html.Div(
                [
                    html.H1('Pick a feature to know about'),
                    dcc.Dropdown(options=graphs,
                                 id='graphs_used', placeholder='Select Symbol...'),
                ],
            )]),
    dbc.Row(
        [
            html.Div(
                        id='My_check_out'
            )]),


	html.Br(),
    dcc.Graph(id='fig'),
])
# @callback(
#     Output(component_id='My_check_out', component_property='value'),
#     [Input(component_id='col_na', component_property='value'),
#     Input(component_id='col_na2', component_property='value'),
#      Input(component_id='col_na3', component_property='value'),
#      Input(component_id='graphs_used', component_property='value')]
# )
# def update_title(a1,a2,a3,a4):
#     if a4=='Histogram':
#         return f"Histogram of {a1}"
#     elif a4=='Scatterplot':
#         return f"Scatterplot of {a1} vs {a2}"
#     elif a4=='Pie Chart':
#         return f"Pie Chart of distribution {a1}"
#     elif a4=='Line chart':
#         return f"Line chart of {a1} vs {a2}"
#     elif a4=='count plot':
#         return f"count plot of {a1} vs {a2}"
#     elif a4=='heat map':
#         return f" heat map of the numerical columns in dastaset"
#     elif a4=='Bar plot':
#         return f"Bar plot of {a1} vs {a2}"
#     elif a4=='Pair plot':
#         return f"pair plot of H1b18.csv dataset"
#     elif a4=='Box plot':
#         return f""


@callback(
    Output(component_id='fig', component_property='figure'),
    [Input(component_id='col_na', component_property='value'),
    Input(component_id='col_na2', component_property='value'),
     Input(component_id='col_na3', component_property='value'),
     Input(component_id='graphs_used', component_property='value')]
)
def update_city_selected(a1,a2,a3,a4):

    if a4=='Histogram':
        fig = px.histogram(data, x=a1 ,title=f"Histogram of {a1}")
    elif a4=='Scatterplot':
        fig = px.scatter(data, x=a1, y=a2, title=f"Scatterplot of {a1} vs {a2}")
    elif a4=='Pie Chart':
        fig = px.pie(data, values=accept_val, names=accept_label, hole=.3, title= f"Pie Chart of distribution {a1}")
    elif a4=='Line chart':
        fig = px.line(data,x=a1, y=a2, color=a3, title=f"Line chart of {a1} vs {a2}")
    elif a4=='count plot':
        fig=px.histogram(data, x=a1, color=a2, title=f"count plot of {a1} vs {a2}")
    elif a4=='heat map':
        fig = px.imshow(data[list2], title=f" heat map of the numerical columns in dastaset")
    elif a4=='Bar plot':
        fig=px.histogram(data, x=a1, y=a2, color=a3, title=f"Bar plot of {a1} vs {a2}")
    elif a4=='Pair plot':
        fig = px.scatter_matrix(data, title=f"pair plot of H1b18.csv dataset")
    elif a4=='Box plot':
        fig = px.box(data, x=a1, color=a2, title=f"Box plot of {a1} vs {a2}")
    elif a4 == 'Regression plot':
        fig = px.scatter(data, x=a1, y=a2,  color=a3, trendline="ols", marginal_x='histogram', marginal_y='histogram',title=f"Regression plot of {a1} vs {a2}")
    return fig
