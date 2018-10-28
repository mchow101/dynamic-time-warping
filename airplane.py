# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 10:53:06 2018

Load, clean, and return dataframe with data from one airplane json file

@author: Mitali
"""

import json
import pandas as pd

def load(filenum):
    #change directory to where you downloaded the data
    s = 'D:\\Mitali\\ML\\airplane_data\\2016-06-20-' + filenum + 'Z.json'
    #load in file
    with open(s) as f:
       data = json.load(f)
    #create a dataframe, with the listed features only
    df = pd.DataFrame(data['acList'])
    features = ['Alt', 'AltT', 'EngMount', 'EngType', 'Engines', 'GAlt', 'Gnd', 'Icao', 'Id', 'InHg', 'Lat', 'Long', 'Mil', 'Mlat', 'PosTime', 'Spd', 'SpdTyp', 'Species', 'TT', 'Trak', 'TrkH', 'Vsi', 'VsiT', 'WTC']
    for col in df:
        num = df[col].isnull().sum()
        if(num > 1000):
            df = df.drop(col, axis=1)
        elif(col not in features):
            df = df.drop(col, axis=1)
    #delete all missing data
    df = df.dropna(axis=0)
    #remove unrealistic data points
    if('Spd' in df.columns):
        df = df[df.Spd < 666]
    if('Alt' in df.columns):
        df = df[df.Alt < 50000]
    if('Vsi' in df.columns):
        df = df[df.Vsi < 5000]
    return df
"""
def getDefault():
    default = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return default
"""