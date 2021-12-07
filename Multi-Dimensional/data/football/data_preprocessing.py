import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from numpyencoder import NumpyEncoder

#displays whole dataframe
pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)

off_2002 = pd.read_csv('./2002off.csv')
def_2002 = pd.read_csv('./2002def.csv')

off_2003 = pd.read_csv('./2003off.csv')
def_2003 = pd.read_csv('./2003def.csv')

off_2004 = pd.read_csv('./2004off.csv')
def_2004 = pd.read_csv('./2004def.csv')

off_2005 = pd.read_csv('./2005off.csv')
def_2005 = pd.read_csv('./2005def.csv')

off_2006 = pd.read_csv('./2006off.csv')
def_2006 = pd.read_csv('./2006def.csv')

off_2007 = pd.read_csv('./2007off.csv')
def_2007 = pd.read_csv('./2007def.csv')

off_2008 = pd.read_csv('./2008off.csv')
def_2008 = pd.read_csv('./2008def.csv')

off_2009 = pd.read_csv('./2009off.csv')
def_2009 = pd.read_csv('./2009def.csv')

off_2010 = pd.read_csv('./2010off.csv')
def_2010 = pd.read_csv('./2010def.csv')

off_2011 = pd.read_csv('./2011off.csv')
def_2011 = pd.read_csv('./2011def.csv')

off_2012 = pd.read_csv('./2012off.csv')
def_2012 = pd.read_csv('./2012def.csv')

off_2013 = pd.read_csv('./2013off.csv')
def_2013 = pd.read_csv('./2013def.csv')

off_2014 = pd.read_csv('./2014off.csv')
def_2014 = pd.read_csv('./2014def.csv')

off_2015 = pd.read_csv('./2015off.csv')
def_2015 = pd.read_csv('./2015def.csv')

off_2016 = pd.read_csv('./2016off.csv')
def_2016 = pd.read_csv('./2016def.csv')

off_2017 = pd.read_csv('./2017off.csv')
def_2017 = pd.read_csv('./2017def.csv')

off_2018 = pd.read_csv('./2018off.csv')
def_2018 = pd.read_csv('./2018def.csv')

off_2019 = pd.read_csv('./2019off.csv')
def_2019 = pd.read_csv('./2019def.csv')

off_2020 = pd.read_csv('./2020off.csv')
def_2020 = pd.read_csv('./2020def.csv')

off_vec = [off_2002,off_2003,off_2004,off_2005,off_2006,off_2007,off_2008,off_2009,off_2010,off_2011,off_2012,off_2013,off_2014,off_2015,off_2016,off_2017,off_2018,off_2019,off_2020]

def_vec = [def_2002,def_2003,def_2004,def_2005,def_2006,def_2007,def_2008,def_2009,def_2010,def_2011,def_2012,def_2013,def_2014,def_2015,def_2016,def_2017,def_2018,def_2019,def_2020]

playoff_win = pd.read_csv('./playoffwin.csv')

name_change_dict = {'San Diego Chargers':'Los Angeles Chargers','Oakland Raiders':'Las Vegas Raiders','Washington Redskins':'Washington Football Team','St. Louis Rams':'Los Angeles Rams'}

inv_name_change = {v: k for k, v in name_change_dict.items()}

'''
tesht = playoff_win[playoff_win['Team'] == 'Buffalo Bills']
tesht = tesht[tesht['Year'] == 2002]
print(tesht.to_numpy()[0][0])
'''

dict_arr = []
for year_ind in range(len(off_vec)):
    for team_ind in range(len(off_vec[0])):
        football_dict = {}
        football_dict['year'] = 2002 + year_ind
        if off_vec[year_ind].iloc[team_ind]['Tm'] in name_change_dict.keys(): 
            football_dict['name'] = name_change_dict[off_vec[year_ind].iloc[team_ind]['Tm']]
            playoff_win_row = playoff_win[playoff_win['Team'] == off_vec[year_ind].iloc[team_ind]['Tm']]
        else: 
            football_dict['name'] = off_vec[year_ind].iloc[team_ind]['Tm']
            if off_vec[year_ind].iloc[team_ind]['Tm'] in inv_name_change.keys():
                playoff_win_row = playoff_win[playoff_win['Team'] == inv_name_change[off_vec[year_ind].iloc[team_ind]['Tm']]]
            else:
                playoff_win_row = playoff_win[playoff_win['Team'] == off_vec[year_ind].iloc[team_ind]['Tm']]
        
        playoff_win_row = playoff_win_row[playoff_win_row['Year'] == (2002 + year_ind)]
        playoff_win_row = playoff_win_row.to_numpy()[0]
        football_dict['Win/Loss Percentage'] = playoff_win_row[1]
        football_dict['Playoffs'] = playoff_win_row[2]

        football_dict['Points For'] = off_vec[year_ind].iloc[team_ind]['PF']
        football_dict['Total Yards For'] = off_vec[year_ind].iloc[team_ind]['Yds']
        football_dict['Yards Per Play For'] = off_vec[year_ind].iloc[team_ind]['Y/P']
        football_dict['Pass Yards For'] = off_vec[year_ind].iloc[team_ind]['Yds.1']
        football_dict['Pass TDs For'] = off_vec[year_ind].iloc[team_ind]['TD']
        football_dict['Rush Yards For'] = off_vec[year_ind].iloc[team_ind]['Yds.2']
        football_dict['Rush TDs For'] = off_vec[year_ind].iloc[team_ind]['TD.1']

        football_dict['Points Against'] = def_vec[year_ind].iloc[team_ind]['PA']
        football_dict['Total Yards Against'] = def_vec[year_ind].iloc[team_ind]['Yds']
        football_dict['Yards Per Play Against'] = def_vec[year_ind].iloc[team_ind]['Y/P']
        football_dict['Pass Yards Against'] = def_vec[year_ind].iloc[team_ind]['Yds.1']
        football_dict['Pass TDs Against'] = def_vec[year_ind].iloc[team_ind]['TD']
        football_dict['Rush Yards Against'] = def_vec[year_ind].iloc[team_ind]['Yds.2']
        football_dict['Rush TDs Against'] = def_vec[year_ind].iloc[team_ind]['TD.1']

        dict_arr.append(football_dict)

with open('football_data.json','w') as outfile:
    json.dump(dict_arr,outfile,indent = '  ',cls=NumpyEncoder)

























