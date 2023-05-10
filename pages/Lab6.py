import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

url='https://raw.githubusercontent.com/rjafari979/Information-Visualization-Data-Analytics-Dataset-/main/weight-height.csv'

df=pd.read_csv(url)
df1=df.head(100)

plt.hist(df.Height)

plt.show()