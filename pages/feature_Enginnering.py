
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash_bootstrap_components as dbc
import dash
from sklearn.decomposition import PCA
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

list=['None','CASE_STATUS','month_CASE_SUBMITTED','month_Decision','EMPLOYMENT_END_DATE','month_EMPLOYMENT_End' ,'CASE_SUBMITTED', 'DECISION_DATE', 'VISA_CLASS',
       'EMPLOYMENT_START_DATE', 'EMPLOYMENT_END_DATE', 'EMPLOYER_NAME',
       'EMPLOYER_STATE', 'JOB_TITLE', 'FULL_TIME_POSITION', 'PREVAILING_WAGE',
       'PW_UNIT_OF_PAY', 'WAGE_RATE_OF_PAY_FROM']
data['FULL_TIME_POSITION'].replace(['Y', 'N'],[1, 0], inplace=True)
data['CASE_STATUS'].replace(['CERTIFIED', 'DENIED','CERTIFIED-WITHDRAWN','WITHDRAWN'],[1, 2,3,4], inplace=True)
data['VISA_CLASS'].replace(['H-1B', 'E-3 Australian','H-1B1 Singapore','H-1B1 Chile'],[1, 2, 3, 4], inplace=True)

layout = html.Div([
    dbc.Row(
            [
                html.Br(),
                dcc.Tabs(id='Questions', value='q1', children=[
                    dcc.Tab(label='PCA', value='q1'),
                    dcc.Tab(label='Download', value='q2')])
    ]),
    html.Br(),
    html.Div(id='layout')
])

question1_layout=html.Div([
    dbc.Row(
            [
                html.H4("Visualization of PCA's explained variance"),
                dcc.Graph(id="graph"),
                html.P("Number of components:"),
                dcc.Slider(
                    id='slider',
                    min=2, max=5, value=3, step=1)
    ]),
    html.Br(),
    html.Div(id='layout')
])
@callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='slider', component_property='value')]
)
def run_and_plot(n_components):
    pca = PCA(n_components=n_components)
    X = data[['FULL_TIME_POSITION', 'CASE_STATUS', 'VISA_CLASS', 'WAGE_RATE_OF_PAY_FROM','PREVAILING_WAGE']]

    components = pca.fit_transform(X)

    var = pca.explained_variance_ratio_.sum() * 100

    labels = {str(i): f"PC {i+1}"
              for i in range(n_components)}

    fig = px.scatter_matrix(
        components,
        dimensions=range(n_components),
        labels=labels,
        title=f'Total Explained Variance: {var:.2f}%')
    return fig

question2_layout=html.Div([
    dbc.Row(
            [

        html.Button("Download CSV", id="btn_csv")
            ]),
        dcc.Download(id="download-dataframe-csv"),
    ]
)
@callback(
    Output(component_id='download-dataframe-csv', component_property='data'),
    [Input(component_id='btn_csv', component_property='n_clicks')],
    prevent_initial_call=True
)

def func(n_clicks):
    return dcc.send_data_frame(data.to_csv, "mydata.csv")


@callback(
    Output(component_id='layout', component_property='children'),
    [Input(component_id='Questions', component_property='value')]
)
def update_city_selected(a1):
    if a1 == 'q1':
        return question1_layout
    elif a1 == 'q2':
        return question2_layout


