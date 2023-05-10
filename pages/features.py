import base64
from scipy.special import expit
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import neurolab as nl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import itertools
from dash.exceptions import PreventUpdate
import warnings
import math
import os

import dash_bootstrap_components as dbc

from dash import Dash, html, dcc
import dash
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