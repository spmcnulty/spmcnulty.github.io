import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
from numpyencoder import NumpyEncoder

#displays whole dataframe
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)

df = pd.read_csv('./fed_data.csv',index_col=0)

#split up percents and raw counts
for i in np.arange(12,26):
    temp_cols = df.iloc[:,i].str.split('\n',expand=True)
    temp_cols[1] = temp_cols[1].str[:-1]
    df.iloc[:,i] = temp_cols[0]
    df.insert(df.shape[1],"percent"+str(i+1),temp_cols[1])

#change to ints and floats
df.iloc[:,:26] = df.iloc[:,:26].astype(int)
df.iloc[:,26:] = df.iloc[:,26:].astype(float)/100

df.insert(df.shape[1],"winner_index",df.iloc[:,12:26].idxmax(axis=1))

df.to_csv('./processed_data_eng.csv')

'''
print(df.iloc[1])

for i in np.arange(12,26):
    print(df.iloc[:]


12 to 25

print(df.iloc[:,0])
'''
