# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 14:42:55 2018

@author: Mitali
"""
import time

t_init = time.time()

import pandas as pd
import airplane
import matplotlib.pyplot as plt
import numpy as np
import DTW
from scipy.signal import argrelextrema
import os
from sklearn.externals import joblib

df = pd.DataFrame()
#load all data - by time, from JSON
for x in range(1, 10):
    if(x%100 < 60 and not x == 305):
        if(x < 10):
            s = '000' + str(x)
        elif(x < 100):
            s = '00' + str(x)
        elif(x < 1000):
            s = '0' + str(x)
        else:
            s = str(x)
        df = df.append(airplane.load(s))
        print s

#sort and split 
df = df.sort_values(by=['Id'])
df = df.sort_values(by=['PosTime'])

#uncomment to load data from presaved files
#
#counter = 0
#p = 30 #number of planes to load
#feature = 'Alt' #feature to use
#path = 'D:\Mitali\ML\planes\\' #folder where data is saved
#
##load data - from PKL files, by plane
#for filename in os.listdir(path):
#    if(counter < p and os.path.getsize(path + filename) > 120000):
#        if(counter == 0):
#            names = [filename]
#        else:
#            names.append(filename)
#        counter = counter + 1
#        print counter
#df = (joblib.load(path + str(names[0]))).sort_values(by=['PosTime']) 
#for x in range(1, len(names)):
#    df = df.append(joblib.load(path + str(names[x])).sort_values(by=['PosTime']))

df = df.reset_index(drop=True)

feature = 'Alt'

#split tracks by relative minima
index = 0
planes = []
planes_icao = []
n = 100 #sample length
s = df.shape[0]
for i in df.Id.unique():
    print i
    hold = index
    store = pd.DataFrame()
    while((index < s) and df.loc[index].Id): 
        index = index  + 1
    store = df[hold:index]
    mins = df.loc[argrelextrema(df.Alt.values, np.less_equal, order=25)[0], feature]
    
    for i in mins.index:
        if(not planes and not index == hold and not i == hold and store[hold:i].shape[0] > n):
            planes = [store[hold:i]]
            planes_icao = [str(store.Icao[hold])]
            hold = i
        elif(not index == hold and not i == hold and store[hold:i].shape[0] > n):
            planes = planes.append(store[hold:i])
            planes_icao = planes_icao.append(str(store.Icao[hold]))
            hold = i
        else:
            index = index + 1

#add all data to a single array
counter = 0
spacefill = np.zeros(n) #first array is spacefiller
data = np.vstack((spacefill, (planes[0])[feature].values[:n]))
for x in range(1, len(planes)):
    data = np.vstack((data, (planes[x])[feature].values[:n]))

#create centroids
centroids=DTW.k_means_clust(data,1,10,4)

#plot each Time Series
counter = 0
results = pd.DataFrame(columns=['data', 'dist', 'icao'])

#uncomment to plot all data
#
#for d in data:
#    plt.figure()
#    k = DTW.DTWDistance(d, centroids[0], 5)
#    if(not counter == 0):
#        plt.plot(d, label=str(counter))
#        results = results.append({'data': d, 'dist': k}, ignore_index=True)
#    counter = counter + 1
#    plt.plot(centroids[0], label='Centroid')
#    plt.title("graph "+str(counter))
#    plt.savefig('D:/Mitali/ML/FullDTWResults/1' + str(counter) + '.png')
#    plt.show()
    

# detect anomalies based on standard deviation threshold

for d in data:
    k = DTW.DTWDistance(d, centroids[0], 5)
    if(not counter == 0):
        results = results.append({'data': d, 'dist': k, 
                                  'icao' : planes_icao[counter - 1]}, 
    ignore_index=True)
    counter = counter + 1

counter = 0
path = 'D:/Mitali/ML/FullDTWResults/' #folder to save data in
for d in data:
    if(not counter == 0 and 
       np.abs(results['dist'][counter - 1] - np.mean(results['dist'])) > 
       np.std(results['dist'])):
        plt.figure()
        plt.plot(d, label=str(counter))
        plt.plot(centroids[0], label='Centroid')
        plt.title("Graph of plane "+str(planes_icao[counter - 1]))
        plt.savefig(path + str(counter) + '.png')
        plt.show()
    counter = counter + 1

# print closest and furthest time series
print 'Furthest Time Series: '
print results['icao'].where(results['dist'] == results['dist'].max()).dropna()
print 'Closest Time Series: '
print results['icao'].where(results['dist'] == results['dist'].min()).dropna()

# uncomment to plot closest centroid 
#
#        if(DTWDistance(i, d, 5) < min_i):
#            min_i = DTWDistance(i, d, 5)
#            hold = i
#    plt.plot(hold)
#    plt.savefig('DTW_Graphs/' + str(counter) + '.png')
#plt.legend(loc='upper right')
#plt.show()

print "Finished!"
print "Time: " + str(time.time() - t_init)

# show distribution of DTW Distances
plt.title("Distribution of DTW Distances")
plt.hist(results['dist'])
