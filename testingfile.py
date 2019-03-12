# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:39:07 2019

@author: Kelly

Divvy Data Project - inserting 2016-2018 data into a dataframe
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

os.chdir('C:/Users/Kelly/Desktop/pymentorship_data/divvy_data')
filepath = ('C:/Users/Kelly/Desktop/pymentorship_data/divvy_data')

#create empty dataframe with headers
testcsv = pd.read_csv(next(os.walk(filepath))[2][1])
headers = testcsv.columns.tolist()
df = pd.DataFrame(columns=headers)

#Add data from CSV file if "Trips" is in the filename
files = next(os.walk(filepath))[2]
for filename in files:
    if 'Trips' in filename:
        print('Reading file: ' + filename)
        temp_df = pd.read_csv(filename)
        if 'start_time' in temp_df.columns:    #if statement to change columns: start_time -> starttime, end_time -> stoptime
            temp_df.rename(columns = {'start_time':'starttime'}, inplace=True)
            print('Renamed starttime column')
        if 'end_time' in temp_df.columns:
            temp_df.rename(columns = {'end_time':'stoptime'}, inplace=True)
            print('Renamed stoptime column')
        df = pd.concat([df, temp_df], ignore_index=True)    #concat function
        print('Success with this file! Length of df: ' + str(len(df)))

#turn df starttime and stoptime columns into timestamps
df['starttime'] =  pd.to_datetime(df['starttime'])    #change starttime col to datetime type; should take about 43 min to process
df['stoptime'] = pd.to_datetime(df['stoptime'])    #change stoptime col to datetimetype; should take about 43 min to process
df['DATE'] = [d.date() for d in df['starttime']]    #make new date column

#add weather columns to df
df = df.join(pd.DataFrame(
    {
        'PRCP': np.nan,
        'SNOW': np.nan,
        'SNWD': np.nan,
        'TMAX': np.nan,
        'TMIN': np.nan,
        'TAVG': np.nan,
    }, index=df.index
))


#pickle this df
df.to_pickle('divvypickle')
#to load df
df = pd.read_pickle('divvypickle')

#load weather data into a df
w_df = pd.read_csv('weather_data.csv')
w_df = w_df.iloc[:,[2,3,4,5,6,7]]   #keep most relevant columns
w_df['TAVG'] = (w_df.TMAX + w_df.TMIN) / 2   #add column for average temperature
w_df['DATE'] = pd.to_datetime(w_df['DATE'])    #change DATE column to timestamp type
w_df['DATE'] = [d.date() for d in w_df['DATE']]   #changing it to same format as df's DATE column

#put weather data into main df
combodf = pd.merge_asof(df, w_df, on='DATE', direction='backward', allow_exact_matches = True)

        





#testing
import time
start = time.time()
combosmalldf = pd.merge_asof(smalldf, temp_wdf['DATE','SNOW'], on='DATE', allow_exact_matches = True)
end = time.time()
print(end - start)

#take part of the combodf (to make smaller df to time process)
smalldf = df.iloc[0:10,]

smalldf['DATE'] = smalldf['DATE'].astype('str')
temp_wdf = w_df
temp_wdf['DATE'] = temp_wdf['DATE'].astype('str')


