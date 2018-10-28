# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 09:04:32 2018

Load and save entire folder of data into a single pickle file

@author: Mitali
"""

import airplane
import pandas as pd
from sklearn.externals import joblib

df = pd.DataFrame()
#go through each available file
for x in range(1, 2360):
    if(x%100 < 60 and not x == 305):
        if(x < 10):
            s = '000' + str(x)
        elif(x < 100):
            s = '00' + str(x)
        elif(x < 1000):
            s = '0' + str(x)
        else:
            s = str(x)
        print s
        df = df.append(airplane.load(s))
#save dataframe
print "Saving pkl..."
joblib.dump(df, 'airplane_data.pkl')
print "Finished!"

"""
#uncomment this section to load data
print "Loading data..."
df = joblib.load('airplane_data.pkl')
print "Finished!"
"""