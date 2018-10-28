# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6
@author: Mitali

Use this code to convert a JSON file from ADS-B to a CSV file
"""

import json
import pandas as pd

def load(filedir, savename):
    #load in JSON file
    with open(filedir) as f:
       data = json.load(f)
       
    #create a dataframe
    df = pd.DataFrame(data['acList'])
    
    #loop through each column of dataframe
    #include the listed features only 
    #and delete all missing data
    features = ['Alt', 'AltT', 'EngMount', 'EngType', 'Engines', 'GAlt', 'Gnd',
                'Icao', 'Id', 'InHg', 'Lat', 'Long', 'Mil', 'Mlat', 'PosTime', 
                'Spd', 'SpdTyp', 'Species', 'TT', 'Trak', 'TrkH', 'Vsi', 
                'VsiT', 'WTC']
    for col in df:
        num = df[col].isnull().sum()
        if(num > 1000):
            df = df.drop(col, axis=1)
        elif(col not in features):
            df = df.drop(col, axis=1)
    df = df.dropna(axis=0)
    
    #write to a CSV file
    df.to_csv(savename)