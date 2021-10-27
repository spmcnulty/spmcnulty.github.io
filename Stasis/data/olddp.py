import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import copy
from numpyencoder import NumpyEncoder

#displays whole dataframe
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)

#read in data
polis_df = pd.read_csv('./polis_sean.csv')

#create null checker
null_check = polis_df.notnull()

#initialize the dictionary to go to output
output_dict = {}
output_dict["type"] = "FeatureCollection"
output_dict["features"] = []

#create a dictionary template for each polis
feat_dict_template = {}
feat_dict_template["type"] = "Feature"
feat_dict_template["geometry"] = {"type":"Point","coordinates":[]}

print(polis_df.loc[1].to_dict())

for i in range(len(polis_df)):
    if null_check.loc[i,'Latitude'] or null_check.loc[i,'Longitude']:
        #create dictionary from row
        to_add = polis_df.loc[i].fillna(-1).to_dict()
        #pop unnamed entries
        to_add.pop('Unnamed: 27')
        #copy dictionary template
        feat_dict = copy.deepcopy(feat_dict_template)
        #pop longitude and latitude and put into the feature dict
        feat_dict["geometry"]["coordinates"].append(float(to_add.pop('Longitude').replace(',','.')))
        feat_dict["geometry"]["coordinates"].append(float(to_add.pop('Latitude').replace(',','.')))


        word_dict = {"Name":to_add.pop("Name"),"Region name":to_add.pop("Region name"),"Pleiades link":to_add.pop("Pleiades link")}

        to_add = {k:float(str(v).replace(',','.')) for (k,v) in to_add.items()}

        to_add = {**to_add,**word_dict}

        #place the rest of the row dict into the feature dict
        feat_dict["properties"] = to_add
        
        #place the feature dict into the output dict
        output_dict["features"].append(feat_dict)

#print(output_dict)

with open('polis_sean.json','w') as outfile:
    json.dump(output_dict,outfile,indent='  ',cls=NumpyEncoder)



'''
prom_1=[]
prom_1_st=[]

prom_2=[]
prom_2_st=[]

prom_3=[]
prom_3_st=[]

for i in range(len(polis_df)):
    if polis_df.loc[i,'staseis'] != 0:
        if not pd.isnull(polis_df.loc[i,'prom 1']):
            prom_1.append(polis_df.loc[i,'prom 1'])
            prom_1_st.append(polis_df.loc[i,'staseis'])
        if not pd.isnull(polis_df.loc[i,'prom 2']):
            prom_2.append(polis_df.loc[i,'prom 2'])
            prom_2_st.append(polis_df.loc[i,'staseis'])
        if not pd.isnull(polis_df.loc[i,'prom 3']):
            prom_3.append(polis_df.loc[i,'prom 3'])
            prom_3_st.append(polis_df.loc[i,'staseis'])

prom_1 = [float(i.replace(',','.'))+1 for i in prom_1]
prom_1_st = [float(i) for i in prom_1_st]

prom_2 = [float(i)+1 for i in prom_2]
prom_2_st = [float(i) for i in prom_2_st]

prom_3 = [float(i)+1 for i in prom_3]
prom_3_st = [float(i) for i in prom_3_st]


plt.plot(prom_1,prom_1_st,'r.',label="Prominance 1")
#plt.plot(prom_2,prom_2_st,'b.',label="Prominance 2")
#plt.plot(prom_3,prom_3_st,'g.',label="Prominance 3")

plt.xlabel("Prominance")
plt.ylabel("Staseis")

#plt.xscale('log')
plt.xlim(0,10)

plt.legend()
plt.show()
'''

'''
tests
print(polis_df.loc[0,'Silver'])
print(type(polis_df.loc[0,'Silver']))
print(np.isnan(polis_df.loc[0,'Silver']))
'''
