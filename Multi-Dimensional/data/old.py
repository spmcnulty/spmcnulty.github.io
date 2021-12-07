import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn.neighbors import KernelDensity
from numpyencoder import NumpyEncoder

#displays whole dataframe
pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)

#read in data
df_countries = pd.read_csv('./homicide_country_download.csv')

#drop unnecessary columns
df_countries.drop("Region",axis=1,inplace=True)
df_countries.drop("Subregion",axis=1,inplace=True)
df_countries.drop("iso3_code",axis=1,inplace=True)
df_countries.drop("Disaggregation",axis=1,inplace=True)
df_countries.drop("Source",axis=1,inplace=True)
df_countries.drop("Footnote",axis=1,inplace=True)

#get rid of other indicators
df_countries = df_countries[df_countries["Indicator"] == "Homicide: # of victims"]
df_countries.drop("Indicator",axis=1,inplace=True)

df_countries = df_countries[df_countries["Gender"] == "Total (all ages)"]
df_countries.drop("Gender",axis=1,inplace=True)

df_countries = df_countries[df_countries["Unit"] == "Rate per  100,000 population"]
df_countries.drop("Unit",axis=1,inplace=True)

ex_comm_NATO = ["Albania","Bulgaria","Croatia","Czechia","Hungary","North Macedonia","Romania","Slovakia","Slovenia"]

ex_soviet_countries = ["Republic of Moldova","Russian Federation","Ukraine","Belarus","Kazakhstan","Uzbekistan","Kyrgyzstan","Tajikistan","Turkmenistan","Georgia","Azerbaijan","Armenia"]

ex_soviet_NATO = ["Lithuania","Latvia","Estonia"]

NATO_countries = ["Belgium","Canada","Denmark","France","Germany","Greece","Iceland","Italy","Luxembourg","Montenegro","Netherlands","Norway","Portugal","Spain","Turkey","United Kingdom","United States of America"]

df_countries = df_countries[df_countries["country"].isin(ex_comm_NATO+ex_soviet_countries+ex_soviet_NATO+NATO_countries)]

#print(len(df_countries))
#print(len(df_countries[df_countries['Year'] == 2002]))
#print(df_countries[df_countries['Year'] == 2002])

dict_arr = []
for i in range(len(df_countries)):

    murder_dict = {}
    murder_dict['year'] = df_countries.iloc[i]['Year']
    murder_dict['country'] = df_countries.iloc[i]['country']
    murder_dict['hom_rate'] = df_countries.iloc[i]['Value']
    if df_countries.iloc[i]['country'] in ex_soviet_countries: murder_dict['cluster'] = 0
    elif df_countries.iloc[i]['country'] in NATO_countries: murder_dict['cluster'] = 1
    elif df_countries.iloc[i]['country'] in ex_comm_NATO: murder_dict['cluster'] = 2
    elif df_countries.iloc[i]['country'] in ex_soviet_NATO: murder_dict['cluster'] = 3
    dict_arr.append(murder_dict)

with open('murder_rate.json','w') as outfile:
    json.dump(dict_arr,outfile,indent='  ',cls=NumpyEncoder)













