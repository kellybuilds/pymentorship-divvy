# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:44:09 2019

@author: Kelly
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import sklearn
import datetime

#testing to see if newly downloaded divvy data has more july data
os.chdir('C:/Users/Kelly/Desktop/pymentorship_data/divvy_data')
filepath = ('C:/Users/Kelly/Desktop/pymentorship_data/divvy_data')


testcsv = pd.read_csv(next(os.walk(filepath))[2][6])
headers = testcsv.columns.tolist()
testdf = pd.DataFrame(columns=headers)

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
        testdf = pd.concat([testdf, temp_df], ignore_index=True)    #concat function
        print('Success with this file! Length of df: ' + str(len(testdf)))
        
#SAVE POINT - pickle this df
testdf.to_pickle('testdf1')
#SAVE POINT - to load df
testdf = pd.read_pickle('testdf1')

#date stuff here
testdf['starttime'] =  pd.to_datetime(testdf['starttime'])    #change starttime col to datetime type; should take about 43 min to process
testdf['date'] = [d.date() for d in testdf['starttime']]    #make date column
testdf['date'] = pd.to_datetime(testdf['date'])
testdf['month'] = testdf['date'].dt.month
testdf['day'] = testdf['date'].dt.dayofweek

#parse out data into season column
seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
month_to_season = dict(zip(range(1,13), seasons))
testdf['season'] = testdf.date.dt.month.map(month_to_season) 

#visualize numeric data
testdf[testdf.dtypes[(testdf.dtypes=="float64")|(testdf.dtypes=="int64")]
            .index.values].hist(figsize=[11,11])

#keep certain columns test
testdf1 = testdf[['starttime', 
                  'stoptime', 
                  'from_station_id',
                  'from_station_name',
                  'to_station_id', 
                  'to_station_name', 
                  'trip_id',
                  'tripduration',
                  'usertype',
                  'date',
                  'month',
                  'day',
                  'season']].copy()

#SAVE POINT - pickle this df
testdf1.to_pickle('testdf1')
#SAVE POINT - to load df
testdf1 = pd.read_pickle('testdf1')




#load weather data into a df
w_df = pd.read_csv('weather_data.csv')
w_df = w_df.iloc[:,[2,3,4,5,6,7]]   #keep most relevant columns
w_df['TAVG'] = (w_df.TMAX + w_df.TMIN) / 2   #add column for average temperature
#put weather data into main df
testdf1['DATE'] = testdf1['date'].astype('str')
w_df['DATE'] = pd.to_datetime(w_df['DATE'])
w_df['DATE'] = w_df['DATE'].astype('str')

testdf2 = testdf1.merge(w_df,
                   how='left',
                   left_on='DATE',
                   right_on='DATE')


