import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
dash.register_page(__name__, path='/', name='Home') # '/' is home page

# page 1 data

pd.set_option("display.max_rows", None, "display.max_columns", None)

data=pd.read_csv('h1b18.csv')
data.dropna(inplace=True)


# removing data which is not necessary
data['CASE_SUBMITTED']=pd.to_datetime(data['CASE_SUBMITTED'])
data['DECISION_DATE']=pd.to_datetime(data['DECISION_DATE'])
data['EMPLOYMENT_START_DATE']=pd.to_datetime(data['EMPLOYMENT_START_DATE'])
data['EMPLOYMENT_END_DATE']=pd.to_datetime(data['EMPLOYMENT_END_DATE'])

data["PREVAILING_WAGE"]=data["PREVAILING_WAGE"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_FROM"]=data["WAGE_RATE_OF_PAY_FROM"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_TO"]=data["WAGE_RATE_OF_PAY_TO"].str.replace(",", "").astype(float)

print(data.nunique().sort_values(ascending=True))
data=data.drop(['SOC_CODE', 'SOC_NAME','CASE_NUMBER','EMPLOYER_POSTAL_CODE','EMPLOYER_CITY','WAGE_RATE_OF_PAY_TO','WAGE_UNIT_OF_PAY'], axis=1)
data.dropna(inplace = True)
print(data.head())
layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(options=data.columns,
                                     id='columns_names')
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig')
                    ], width=12
                )
            ]
        )
    ]
)


@callback(
    Output('line-fig', 'figure'),
    Input('columns_names', 'value')
)
def update_graph(value):
    if value == 'CASE_STATUS':
        fig = px.histogram(data, x='CASE_STATUS')
    elif value == 'CASE_SUBMITTED':
        fig = px.histogram(data, x='CASE_SUBMITTED')
    elif value == 'DECISION_DATE':
        fig = px.histogram(data, x='DECISION_DATE')
    elif value == 'VISA_CLASS':
        fig = px.histogram(data, x='VISA_CLASS')
    elif value =='EMPLOYMENT_START_DATE':
        fig = px.histogram(data, x='EMPLOYMENT_START_DATE')
    elif value == 'EMPLOYER_STATE':
        fig = px.histogram(data, x='EMPLOYER_STATE')
    elif value== 'EMPLOYMENT_END_DATE':
        fig = px.histogram(data, x='EMPLOYMENT_END_DATE')
    elif value == 'EMPLOYER_NAME':
        fig = px.histogram(data, x='EMPLOYER_NAME')
    elif value == 'JOB_TITLE':
        fig = px.histogram(data, x='JOB_TITLE')
    elif value == 'FULL_TIME_POSITION':
        fig = px.histogram(data, x='FULL_TIME_POSITION')
    elif value == 'PREVAILING_WAGE':
        fig = px.histogram(data, x='PREVAILING_WAGE')
    elif value == 'PW_UNIT_OF_PAY':
        fig = px.histogram(data, x='PW_UNIT_OF_PAY')
    else:
        fig = px.histogram(data, x='WAGE_RATE_OF_PAY_FROM')
    return fig