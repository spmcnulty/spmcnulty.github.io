import numpy as np
import matplotlib as plt
import xml.etree.ElementTree as ET
import pandas as pd
from numpyencoder import NumpyEncoder

#displays whole dataframe
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)

#get candidates and their votes
xml_tree = ET.parse('./данные_одно.xml')
root = xml_tree.getroot()

result_dict = {}

for i in range(225):
    name = root[i].attrib['name'].split(' – ')[-1]
    
    if name in result_dict:
        name_counter = 0
        name += str(name_counter)
        while name in result_dict:
            name_counter += 1
            name = name[:-1]+str(name_counter)

    result_dict[name] = {}
    for j in range(12,len(root[i].getchildren())):
        result_dict[name][root[i][j][0].text] = root[i][j][1].text

#get candidates and their parties
party_dict = {}

file = open('single_mand_part','r')


while True:
    first_line = file.readline()
    first_line = first_line.split('\xa0- ')

    second_line = file.readline()
    second_line = second_line.split('\xa0-\xa0')

    if not first_line[0] or not second_line[0]:
        break

    index = int(first_line[0][2:])-1
    name = first_line[1][:-1].split(' ')[0]

    if name in party_dict and index not in party_dict[name]:
        name_counter = 0
        name += str(name_counter)
        while name in party_dict and index not in party_dict[name]:
            name_counter += 1
            name = name[:-1]+str(name_counter)
    if name not in party_dict:
        party_dict[name] = {index:'index'}
    
    candidate = second_line[0]
    party = second_line[1][:-1]
    party_dict[name][candidate] = party

#coordinate parties to their results in each okrug
party_result_dict = {}

for okrug in party_dict:
    index = list(party_dict[okrug].keys())[list(party_dict[okrug].values()).index('index')]
    party_result_dict[index] = {}

    for candidate in party_dict[okrug]:
        if candidate != index:
            if candidate in result_dict[okrug]:
                if party_dict[okrug][candidate] in party_result_dict[index]:
                    party_result_dict[index][party_dict[okrug][candidate]] = str(int(party_result_dict[index][party_dict[okrug][candidate]]) + int(result_dict[okrug][candidate]))
                else: party_result_dict[index][party_dict[okrug][candidate]] = result_dict[okrug][candidate]
            else:
                pass
                #print(candidate,'from party_dict in okrug',okrug,'not in result_dict')

for okrug in result_dict:
    for candidate in result_dict[okrug]:
        if candidate not in party_dict[okrug]:
            pass
            #print(candidate,'from result_dict in okrug',okrug,'not in party_dict')

parties = {}
for okrug in party_result_dict:
    for party in party_result_dict[okrug].keys():
        if party not in parties:
            parties[party] = len(parties)

trans_dict = {'ЛДПР': 15, 'Новые люди': 16, 'КПРФ': 13, 'Самовыдвижение': 27, 'Справедливая Россия': 18, 'Коммунисты России (КПКР)': 22, 'Партия пенсионеров': 26, 'Партия свободы и справедливости': 21, 'Единая Россия': 17, 'Зеленые': 14, 'Партия Роста': 20, 'Яблоко': 19, 'Родина': 25, 'Гражданская Платформа': 23, 'Зеленая альтернатива': 24}

single_man_df = pd.DataFrame(0,index=(['Сумма']+np.arange(1,226).tolist()),columns = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27])

for okrug in party_result_dict:
    for party in party_result_dict[okrug]:
        single_man_df[trans_dict[party]][okrug+1] = party_result_dict[okrug][party]

single_man_df.loc['Сумма',:] = single_man_df.sum()


for i in np.arange(13,28):
    temp_cols = single_man_df.loc[:,i]/single_man_df.iloc[:,:17].sum(axis=1)
    single_man_df.insert(single_man_df.shape[1],"percent"+str(i),temp_cols)

single_man_df.insert(single_man_df.shape[1],"winner_index",single_man_df.iloc[:,:17].idxmax(axis=1))

print(single_man_df.iloc[:,17:-1].sum(axis=1))

#single_man_df.to_csv('./sing_man_eng.csv')

'''
print(single_man_df)

party_result_dict[1] = 3

print(list(party_result_dict.keys())[list(party_result_dict.values()).index(3)])

same_dict = ['Центральный0', 'Центральный1', 'Красноармейский0', 'Центральный2', 'Центральный3', 'Южный0', 'Ростовский0', 'Новомосковский0', 'Центральный4', 'Северный0', 'Центральный5', 'Южный1','Центральный','Красноармейский','Южный','Ростовский','Новомосковский','Северный']

print("PARTY DICT!!!!!")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
for key in same_dict:
    print(key)
    print(party_dict[key])
    print()
    print()

print("RESULT DICT!!!!!")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~")
for key in same_dict:
    print(key)
    print(result_dict[key])
    print()
    print()

party_ind = []
for key in party_dict.keys():
    if key[-1] in '0123456789': party_ind.append(key)
result_ind = []
for key in result_dict.keys():
    if key[-1] in '0123456789': result_ind.append(key)

print('party',party_ind)
print('result',result_ind)






print(len(party_dict.keys()))
print(len(result_dict.keys()))


print(party_dict[224])
print(result_dict[224])

#count1 = 0
#count2 = 0



non_match_array = []
ind_match_array = []

for okrug in result_dict: 

    if len(result_dict[okrug].keys()) != len(party_dict[okrug].keys())-1:
        if okrug[-1] in '0123456789':
            ind_match_array.append(okrug)
        else:
            non_match_array.append(okrug)


print('ind',party_dict['Стерлитамакский'])
print('non',result_dict['Стерлитамакский'])



#for okrug in party_dict: count2 += len(party_dict[okrug].keys())

#print('count1',count1)
#print('count2',count2)

#print(party_dict)


#print(root[0])
#print(root[224][12][1].text)
#print(root[3].attrib)
'''
