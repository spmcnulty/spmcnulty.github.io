import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import copy
from numpyencoder import NumpyEncoder

df_crossovers = pd.read_csv('./crossovers.csv',index_col=0)
df_crossovers.fillna(value=0.0,inplace=True)

json_dict = {}
json_dict['nodes'] = []
json_dict['links'] = []


for i in range(len(df_crossovers)):
    node_dict = {}
    node_dict['name'] = df_crossovers.index[i]
    node_dict['Primary Series Genre'] = df_crossovers['group'][i]
    node_dict['Disjoint Graphs Formed'] = df_crossovers['disjoint'][i]
    node_dict['index'] = i
    node_dict['Crossovers (Node Degree)'] = 0
    json_dict['nodes'].append(node_dict)

    #first index is "group" category, only consider "top half" of matrix
    for j in range(i+3,len(df_crossovers)+2):
        if df_crossovers.iloc[i].iloc[j] == 1:
            link_dict = {}
            link_dict['source'] = i
            link_dict['target'] = j-2
            link_dict['value'] = 1
            json_dict['links'].append(link_dict)

for i in range(len(json_dict['links'])):
    link = json_dict['links'][i]
    json_dict['nodes'][link['source']]['Crossovers (Node Degree)'] += 1
    json_dict['nodes'][link['target']]['Crossovers (Node Degree)'] += 1

with open('crossovers_new.json','w') as outfile:
    json.dump(json_dict,outfile,indent='  ',cls=NumpyEncoder)

#Calculate Average Degree
avg_cross_dict = {}
avg_cross_dict['Live Action Comedy'] = [0,0]
avg_cross_dict['Live Action Drama'] = [0,0]
avg_cross_dict['Superhero'] = [0,0]
avg_cross_dict['Animated'] = [0,0]
avg_cross_dict['Film'] = [0,0]

avg_dis_dict = copy.deepcopy(avg_cross_dict)

for i in range(len(json_dict['nodes'])):
    node = json_dict['nodes'][i]
    avg_cross_dict[node['Primary Series Genre']][0] += node['Crossovers (Node Degree)']
    avg_cross_dict[node['Primary Series Genre']][1] += 1

    avg_dis_dict[node['Primary Series Genre']][0] += node['Disjoint Graphs Formed']
    avg_dis_dict[node['Primary Series Genre']][1] += 1



for arr in avg_cross_dict:
    avg_cross_dict[arr][0] /=avg_cross_dict[arr][1]
    avg_dis_dict[arr][0] /= avg_dis_dict[arr][1]

print(avg_cross_dict)
print("~~~~~~~~~~~~~~~")
print(avg_dis_dict)




#print(df_crossovers['group'][0])
#print(df_crossovers)
#print(df_crossovers.iloc[0])



