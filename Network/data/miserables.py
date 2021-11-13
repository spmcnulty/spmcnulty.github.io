import numpy as np
import json

with open('miserables.json','r') as infile:
    mis = json.load(infile)

with open('miserables.json','w') as outfile:
    json.dump(mis,outfile,indent='  ')
