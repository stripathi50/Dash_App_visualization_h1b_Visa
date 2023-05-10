import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import base64
from scipy.special import expit
import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
import plotly as plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import plotly.figure_factory as ff
import dash_html_components as html
import base64
import io
import plotly.graph_objs as go
import dash_table

# data loading


pd.set_option("display.max_rows", None, "display.max_columns", None)

data = pd.read_csv('h1b18.csv')
data.dropna(inplace=True)
print(data.info())


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

df_heatmap = data.groupby('EMPLOYER_STATE')['CASE_STATUS'].count()
print(df_heatmap)
accept_arr = data['CASE_STATUS'].value_counts()
print(accept_arr)
accept_val = list(accept_arr)[0:4]
accept_label = list(accept_arr.index)[0:4]

sns.heatmap(data.corr())
plt.title("Heat map of the numerical data in H1b18 Dataset")
plt.show()


print(data.describe())
print(data. info())
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("H1B1 Visa Analysis 2018",
                         style={'fontSize':50, 'textAlign':'center'}))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)

app.run_server(
    port=8061,
    host='0.0.0.0'
)
