# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 10:03:29 2018

@author: Mitali

Source: http://nbviewer.jupyter.org/github/alexminnaar/time-series-classification-and-clustering/blob/master/Time%20Series%20Classification%20and%20Clustering.ipynb
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from sklearn.externals import joblib
import os

#function to find dynamic time warping distance
def DTWDistance(s1, s2,w):
    DTW={}
    
    w = max(w, abs(len(s1)-len(s2)))
    #prepare array
    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0
    #fill array with corresponding DTW values
    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= (s1[i]-s2[j])**2
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])
    #return distance
    return np.sqrt(DTW[len(s1)-1, len(s2)-1])
#faster DTW method
def LB_Keogh(s1,s2,r):
    LB_sum=0
    for ind,i in enumerate(s1):
        
        lower_bound=min(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        upper_bound=max(s2[(ind-r if ind-r>=0 else 0):(ind+r)])
        
        if i>upper_bound:
            LB_sum=LB_sum+(i-upper_bound)**2
        elif i<lower_bound:
            LB_sum=LB_sum+(i-lower_bound)**2
    
    return np.sqrt(LB_sum)

from sklearn.metrics import classification_report
#classification algorithm
def knn(train,test,w):
    preds=[]
    for ind,i in enumerate(test):
        min_dist=float('inf')
        closest_seq=[]
        #print ind
        for j in train:
            if LB_Keogh(i[:-1],j[:-1],5)<min_dist:
                dist=DTWDistance(i[:-1],j[:-1],w)
                if dist<min_dist:
                    min_dist=dist
                    closest_seq=j
        preds.append(closest_seq[-1])
    return classification_report(test[:,-1],preds)

#uncomment for training datasets
#train = np.genfromtxt('datasets/train.csv', delimiter='\t')
#test = np.genfromtxt('datasets/test.csv', delimiter='\t')
#print knn(train,test,4)
    
import random
#clustering algorithm
def k_means_clust(data,num_clust,num_iter,w=5):
    centroids=random.sample(data,num_clust)
    counter=0
    for n in range(num_iter):
        counter+=1
        print counter
        assignments={}
        #assign data points to clusters
        for ind,i in enumerate(data):
            min_dist=float('inf')
            closest_clust=None
            for c_ind,j in enumerate(centroids):
                if LB_Keogh(i,j,5)<min_dist:
                    cur_dist=DTWDistance(i,j,w)
                    if cur_dist<min_dist:
                        min_dist=cur_dist
                        closest_clust=c_ind
            if closest_clust in assignments:
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[]
    
        #recalculate centroids of clusters
        for key in assignments:
            clust_sum=0
            for k in assignments[key]:
                clust_sum=clust_sum+data[k]
            centroids[key]=[m/len(assignments[key]) for m in clust_sum]
    return centroids
#uncomment for training data
#train = np.genfromtxt('datasets/train.csv', delimiter='\t')
#test = np.genfromtxt('datasets/test.csv', delimiter='\t')
#data=np.vstack((train[:,:-1])) #,test[:,:-1]))

def run(n, feature):
#    my_list = ((joblib.load('planes/plane11152325.pkl')).sort_values(by=['PosTime'])[[feature]]
#    my_list = my_list.append(joblib.load('planes/plane10808234.pkl'))
#    my_list = my_list.append(joblib.load('planes/plane7604013.pkl'))
#    
#    for i in range(len(my_list)):
#        my_list[i] = my_list[i])
#        my_list[i] = my_list[i]
#    
#    data = np.vstack((my_list[i][feature].values[:300], my_list[i][feature].values[:300], my_list[i][feature].values[:300]))
    #print data
#    data = data
    '''
    nums = [11152325, 10808234, 10807414, 7604013]
    data = np.vstack((((joblib.load('planes/plane' + str(nums[0]) + '.pkl')).sort_values(by=['PosTime'])[feature].values[:300]), 
                     ((joblib.load('planes/plane' + str(nums[1]) + '.pkl')).sort_values(by=['PosTime'])[feature].values[:300])))
    for x in range(2, len(nums)):
        data = np.vstack((data, ((joblib.load('planes/plane' + str(nums[x]) + '.pkl')).sort_values(by=['PosTime'])[feature].values[:300])))
    print data
    '''
    counter = 0
    for filename in os.listdir('planes'):
        if(counter < n and os.path.getsize('D:\Mitali\ML\planes\\' + filename) > 120000):
            if(counter == 0):
                names = [filename]
            else:
                names.append(filename)
            counter = counter + 1
    data = np.vstack((((joblib.load('planes/' + str(names[0]))).sort_values(by=['PosTime'])[feature].values[:300]), 
                     ((joblib.load('planes/' + str(names[1]))).sort_values(by=['PosTime'])[feature].values[:300])))
    for x in range(2, len(names)):
        data = np.vstack((data, ((joblib.load('planes/' + str(names[x]))).sort_values(by=['PosTime'])[feature].values[:300])))
    print data
    
    centroids=k_means_clust(data,6,10,4)
    
    counter = 0
    for d in data:
    #    min_i = 100
    #    hold = 0
        plt.figure()
        plt.plot(d)
        plt.title((joblib.load('planes/' + str(names[counter]))))
        for i in centroids:
            plt.plot(i)
    #        if(DTWDistance(i, d, 5) < min_i):
    #            min_i = DTWDistance(i, d, 5)
    #            hold = i
    #    plt.plot(hold)
        plt.savefig('DTW_Graphs/' + str(names[counter]) + '.png')
        counter = counter + 1
        print counter
    print "Finished!"
