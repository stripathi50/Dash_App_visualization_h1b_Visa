import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/', name='About')  # '/' is home page

# page 1 data

pd.set_option("display.max_rows", None, "display.max_columns", None)

data = pd.read_csv('h1b18.csv')
data.dropna(inplace=True)

# removing data which is not necessary
data['CASE_SUBMITTED'] = pd.to_datetime(data['CASE_SUBMITTED'])
data['DECISION_DATE'] = pd.to_datetime(data['DECISION_DATE'])
data['EMPLOYMENT_START_DATE'] = pd.to_datetime(data['EMPLOYMENT_START_DATE'])
data['EMPLOYMENT_END_DATE'] = pd.to_datetime(data['EMPLOYMENT_END_DATE'])

data["PREVAILING_WAGE"] = data["PREVAILING_WAGE"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_FROM"] = data["WAGE_RATE_OF_PAY_FROM"].str.replace(",", "").astype(float)
data["WAGE_RATE_OF_PAY_TO"] = data["WAGE_RATE_OF_PAY_TO"].str.replace(",", "").astype(float)

# print(data.nunique().sort_values(ascending=True))
data = data.drop(['SOC_CODE', 'EMPLOYMENT_END_DATE', 'SOC_NAME', 'CASE_NUMBER', 'EMPLOYER_POSTAL_CODE', 'EMPLOYER_CITY',
                  'WAGE_RATE_OF_PAY_TO', 'WAGE_UNIT_OF_PAY'], axis=1)
data.dropna(inplace=True)


# print(data.head())


layout = html.Div([
    dbc.Row(
                    [
                        html.Div([
                            html.H1('About'),
                            html.Div([
                                html.P('H-1B visa is a visa in the United States under the Immigration and Nationality Act, section 101(a)(15)(H) that allows U.S. employers to temporarily employ foreign workers in specialty occupations.'
                                       ' A specialty occupation requires the application of specialized knowledge and a bachelor’s degree or the equivalent of work experience.'),
                                html.P('The H-1B Dataset selected for this project contains data from employer’s Labor Condition Application and the case certification determinations processed by the Office of Foreign Labor Certification (OFLC). '
                                       'The Labor Condition Application (LCA) is a document that a perspective H-1B employer files with U.S. Department of Labor Employment and Training Administration (DOLETA) when it seeks to employ non-immigrant '
                                       'workers at a specific job occupation in an area of intended employment for not more than three years. '
                                       'The datasets are from the Department of Labors website.'),
                            ])
                        ])
                    ]),
        dbc.Row(
            [
                html.Div(
                    [
                        html.H1('Pick a feature to know about'),
                        dcc.Dropdown(options=data.columns,
                                     id='columns_names', placeholder='Select Symbol...'),
                    ],
                )]),
                html.Br(),
                dbc.Row(
                    [
                        html.Div(id='My_out'),
                    ]),


    ]
)


@callback(
    Output(component_id='My_out', component_property='children'),
    Input(component_id='columns_names', component_property='value')
)
def update_theinput(value):
    feature_explain = {"CASE_STATUS": "Status of the case. A categorical variable with 4 unique values ",
                       "CASE_SUBMITTED": " Case submission is a date time variable signifies when the application was submitted",
                       "DECISION_DATE": "Decision date is a date time variable signifies when the decision was made for submitted application",
                       "VISA_CLASS": "Visa class is categorical variable which descibes the visa class of the applicant",
                       "EMPLOYMENT_START_DATE": "Employement start date variable is date time variable. shows the employment start date of applicant",
                       "EMPLOYER_STATE": "Employer state is also a categorical vairable. show the state of the employer",
                       "EMPLOYER_NAME": "Employer name is the categorical variable show the name of the employer",
                       "JOB_TITLE": "Job title is a categorical variable shows the title of the job ",
                       "FULL_TIME_POSITION": "Full time Position is the categorical variable shows the if employee has full time job or not",
                       "PREVAILING_WAGE": "Wage of the employee based on the PW_UNIT_OF_PAY",
                       "PW_UNIT_OF_PAY": "Unit of payment can be year, month, weekly or biweekly",
                       "WAGE_RATE_OF_PAY_FROM": "wage rate to pay the employee"}
    return f"{feature_explain.get(value)}"

