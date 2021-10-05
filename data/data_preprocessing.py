import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from sklearn.neighbors import KernelDensity

#displays whole dataframe
#pd.set_option("display.max_rows", None, "display.max_columns", None)
#displays who numpy array
#np.set_printoptions(threshold=np.inf)


#read in data
df_2021 = pd.read_csv('./pass_locations.csv')
df_rest = pd.read_csv('./all_pass_locations.csv')

#remove non-rookies from df_rest

#2017
season_2017 = df_rest[df_rest["season"] == 2017]
rookies_2017 = ["Mitchell Trubisky", "Patrick Mahomes","Derrick Watson","DeShone Kizer","Casey Beathard","Nathan Peterman"]
season_2017 = season_2017[season_2017["name"].isin(rookies_2017)]

#2018
season_2018 = df_rest[df_rest["season"] == 2018]
rookies_2018 = ["Baker Mayfield","Sam Darnold","Joshua Allen","Joshua Rosen","Lamar Jackson","Kyle Allen"]
season_2018 = season_2018[season_2018["name"].isin(rookies_2018)]

#2019
season_2019 = df_rest[df_rest["season"] == 2019]
rookies_2019 = ["Kyler Murray","Daniel Jones","Dwayne Haskins","Drew Lock","Will Grier","Ryan Finley","Gardner Minshew","David Blough","Devlin Hodges"]
season_2019 = season_2019[season_2019["name"].isin(rookies_2019)]

#2020
season_2020 = df_rest[df_rest["season"] == 2020]
rookies_2020 = ["Joe Burrow","Tua Tagovailoa","Justin Herbert","Jalen Hurts","Jake Luton","Ben DiNucci"]
season_2020 = season_2020[season_2020["name"].isin(rookies_2020)]

all_years = pd.concat([season_2017,season_2018,season_2019,season_2020])

#Add in bust information
busts = ["Mitchell Trubisky","DeShone Kizer","Casey Beathard","Nathan Peterman","Sam Darnold","Joshua Rosen","Kyle Allen","Dwayne Haskins","Drew Lock","Will Grier","Ryan Finley","Gardner Minshew","David Blough","Devlin Hodges","Jake Luton","Ben DiNucci"]
bust_df = all_years[all_years["name"].isin(busts)]
bust_df.insert(7,"bust","Y")

steals = ["Patrick Mahomes","Derrick Watson","Baker Mayfield","Joshua Allen","Lamar Jackson","Kyler Murray","Daniel Jones","Joe Burrow","Tua Tagovailoa","Justin Herbert","Jalen Hurts"]
steal_df = all_years[all_years["name"].isin(steals)]
steal_df.insert(7,"bust","N")

all_years = pd.concat([bust_df,steal_df])

#process 2021 data
df_2021 = df_2021.drop(labels="game_id",axis=1)
df_2021.insert(6,"season",2021)
df_2021.insert(7,"bust","U")

#concat 2021 data to previous years
all_years = pd.concat([all_years,df_2021])


#Bin the pass data to rasterize it, also get raw x and y values for kde

'''
A note on granularity, the field size in the y direction is -10 yards behind the LOS to 60 years in front of the LOS and the field 
size in the x direction is from roughly -30 yards at the left out of bounds mark to 30 at the right out of bounds mark.  Thus the default
bin size is one square yard.  A larger granularity decreases this by increasing the number of bins and a small granularity increases this by
decreasing the number of bins.
'''
granularity = 0.5

num_y_bins = int(70*granularity)
y_bin_sep = 70/num_y_bins
num_x_bins = int(60*granularity)
x_bin_sep = 60/num_x_bins

bust_mat = np.zeros((num_x_bins,num_y_bins))
steal_mat = np.zeros((num_x_bins,num_y_bins))
new_mat = np.zeros((num_x_bins,num_y_bins))

x_bust = np.zeros(len(bust_df))
y_bust = np.zeros(len(bust_df))
bust_index = 0

x_steal = np.zeros(len(steal_df))
y_steal = np.zeros(len(steal_df))
steal_index = 0

x_new = np.zeros(len(df_2021))
y_new = np.zeros(len(df_2021))
new_index = 0

for i in range(len(all_years)):
    y_index = int((all_years.iloc[i]['y']+10)//y_bin_sep)
    x_index = int((all_years.iloc[i]['x']+30)//x_bin_sep)

    iden = all_years.iloc[i]["bust"]

    if iden == 'Y': 
        bust_mat[x_index,y_index]+=1
        x_bust[bust_index] = all_years.iloc[i]['x']
        y_bust[bust_index] = all_years.iloc[i]['y']
        bust_index += 1
    elif iden == 'N': 
        steal_mat[x_index,y_index]+=1
        x_steal[steal_index] = all_years.iloc[i]['x']
        y_steal[steal_index] = all_years.iloc[i]['y']
        steal_index += 1
    else: 
        new_mat[x_index,y_index]+=1
        x_new[new_index] = all_years.iloc[i]['x']
        y_new[new_index] = all_years.iloc[i]['y']
        new_index += 1

#uncomment to test plot the binning, current set to plotting steals
'''
plt.imshow(steal_mat, cmap='hot')
plt.show()
'''

#transform matricies for correct orientation
bust_mat = np.transpose(bust_mat)
bust_mat = np.flip(bust_mat,axis=0)

steal_mat = np.transpose(steal_mat)
steal_mat = np.flip(steal_mat,axis=0)

new_mat = np.transpose(new_mat)
mew_mat = np.flip(new_mat,axis=0)

#Kernel Density Estimate

'''
Function from here: https://stackoverflow.com/questions/41577705/how-does-2d-kernel-density-estimation-in-python-sklearn-work
'''

def kde2D(x, y, bandwidth, xbins=100j, ybins=100j, **kwargs):
    """Build 2D kernel density estimate (KDE)."""

    # create grid of sample locations (default: 100x100)
    xx, yy = np.mgrid[x.min():x.max():xbins,
                      y.min():y.max():ybins]

    xy_sample = np.vstack([yy.ravel(), xx.ravel()]).T
    xy_train  = np.vstack([y, x]).T

    kde_skl = KernelDensity(bandwidth=bandwidth, **kwargs)
    kde_skl.fit(xy_train)

    # score_samples() returns the log-likelihood of the samples
    z = np.exp(kde_skl.score_samples(xy_sample))
    return np.reshape(z, xx.shape)
    #return xx, yy, np.reshape(z, xx.shape)

bust_kde = kde2D(x_bust, y_bust, 2, xbins=600j, ybins=700j)
bust_kde = bust_kde/np.sum(bust_kde)
bust_kde = np.transpose(bust_kde)
bust_kde = np.flip(bust_kde, axis=0)
print("Bust KDE Done!")
print("Normalized Bust Max:",(bust_kde/np.sum(bust_kde)).max())

steal_kde = kde2D(x_steal,y_steal, 2, xbins=600j, ybins=700j)
steal_kde = steal_kde/np.sum(steal_kde)
steal_kde = np.transpose(steal_kde)
steal_kde = np.flip(steal_kde, axis=0)
print("Steal KDE Done!")
print("Normalized Steal Max:",(steal_kde/np.sum(steal_kde)).max())

new_kde = kde2D(x_new,y_new, 2, xbins=600j, ybins=700j)
new_kde = new_kde/np.sum(new_kde)
new_kde = np.transpose(new_kde)
new_kde = np.flip(new_kde, axis=0)
new_kde = new_kde/np.sum(new_kde)
print("Rookie KDE Done!")
print("Normalized Rookie Max:",(new_kde/np.sum(new_kde)).max())

#flatten data, normalize, and turn into a list for WebStorm

bust_mat = bust_mat.flatten()
bust_mat = bust_mat/bust_mat.max()
bust_mat = bust_mat.tolist()

bust_kde = bust_kde.flatten()
bust_kde = bust_kde/bust_kde.max()
bust_kde = bust_kde.tolist()

steal_mat = steal_mat.flatten()
steal_mat = steal_mat/steal_mat.max()
steal_mat = steal_mat.tolist()

steal_kde = steal_kde.flatten()
steal_kde = steal_kde/steal_kde.max()
steal_kde = steal_kde.tolist()

new_mat = new_mat.flatten()
new_mat = new_mat/new_mat.max()
new_mat = new_mat.tolist()

new_kde = new_kde.flatten()
new_kde = new_kde/new_kde.max()
new_kde = new_kde.tolist()

#put in dictionary form for json
bust_out = {}
bust_out["width"] = num_x_bins
bust_out["height"] = num_y_bins
bust_out["values"] = bust_mat

bust_kde_out = {}
bust_kde_out["width"] = 600
bust_kde_out["height"] = 700
bust_kde_out["values"] = bust_kde

steal_out = bust_out.copy()
steal_out["values"] = steal_mat

steal_kde_out = bust_kde_out.copy()
steal_kde_out["values"] = steal_kde

new_out = bust_out.copy()
new_out["values"] = new_mat

new_kde_out = bust_kde_out.copy()
new_kde_out["values"] = new_kde

#Uncomment to output binned data
'''
with open('bust_binned.json','w') as outfile:
    json.dump(bust_out,outfile)

with open('steal_binned.json','w') as outfile:
    json.dump(steal_out,outfile)

with open('new_binned.json','w') as outfile:
    json.dump(new_out,outfile)
'''

with open('bust_kde.json','w') as outfile:
    json.dump(bust_kde_out,outfile)

with open('steal_kde.json','w') as outfile:
    json.dump(steal_kde_out,outfile)

with open('new_kde.json','w') as outfile:
    json.dump(new_kde_out,outfile)


#Uncomment to plot raw data points, currently set to plotting 2021 rookies
'''
test = all_years[all_years["bust"] == "U"]

comps = test[test["pass_type"] == "COMPLETE"]
ints = test[test["pass_type"] == "INTERCEPTION"]
incs = test[test["pass_type"] == "INCOMPLETE"]
tds = test[test["pass_type"] == "TOUCHDOWN"]

#comps = comps[comps["name"]=="Trevor Lawrence"]
#comps = comps[comps["week"]==1]

#ints = ints[ints["name"]=="Trevor Lawrence"]
#ints = ints[ints["week"]==1]

#incs = incs[incs["name"]=="Trevor Lawrence"]
#incs = incs[incs["week"]==1]

#tds = tds[tds["name"]=="Trevor Lawrence"]
#tds = tds[tds["week"]==1]


minX = test['x'].min()
maxX = test['x'].max()

plt.title("2021")
plt.plot(np.linspace(minX,maxX,10),np.zeros(10),'b')
plt.plot(comps['x'],comps['y'],'g.',label="Completions")
plt.plot(incs['x'],incs['y'],'.',color='y',label="Incompletions")
plt.plot(ints['x'],ints['y'],'r.',label="Interceptions")
plt.plot(tds['x'],tds['y'],'m.',label="Touchdowns")
plt.legend()
plt.show()
'''
