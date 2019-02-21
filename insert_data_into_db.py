# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:01:16 2019

@author: Kelly

A script to put Divvy data into a SQLite database
"""
#setup
import os
import sqlite3
import pandas as pd

os.chdir('C:/Users/Kelly/Dropbox/pymentorship/project/sqlite_db')



#USE ONCE - create db, its table - setup
conn = sqlite3.connect('divvy_db.db')
c = conn.cursor()
#create table with columns
c.execute('CREATE TABLE data (trip_id, starttime, stoptime, bikeid, tripduration, from_station_id, from_station_name, to_station_id, to_station_name, usertype, gender, birthday);')
c.close()
conn.close()



#insert divvy data into db; recursively go through all excel files and enter data into database
filepath = ('C:/Users/Kelly/Dropbox/pymentorship/project')
files = next(os.walk(filepath))[2]

conn = sqlite3.connect('divvy_db.db')   #connects to db and setup
c = conn.cursor()

dataSQL = '''INSERT INTO data(trip_id, starttime, stoptime, bikeid, tripduration, from_station_id, from_station_name, to_station_id, to_station_name, usertype, gender, birthday)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?)'''

for filename in files:
    if 'Trips' in filename:
        print('Reading file: ' + filename)
        temp_df = pd.read_csv(filepath + '/' + filename)
        for i, row in temp_df.iterrows():
            trip_id = row[0]
            starttime = row[1]
            stoptime = row[2]
            bikeid = row[3]
            tripduration = row[4]
            from_station_id = row[5]
            from_station_name = row[6]
            to_station_id = row[7]
            to_station_name = row[8]
            usertype = row[9]
            gender = row[10]
            birthday = row[11]
            row = [trip_id, starttime, stoptime, bikeid, tripduration, from_station_id, from_station_name, to_station_id, to_station_name, usertype, gender, birthday]
            print(row)
            c.execute(dataSQL, row)
            conn.commit()

c.close()
conn.close()








#testing section
p = "C:/Users/Kelly/Dropbox/pymentorship/project"
test_df = pd.read_csv(p + '/Divvy_Trip_2013.csv')

for row in test_df.iterrows():
    print(row)

for filename in files:
    if 'Trips' in filename:
        temp=pd.read_csv(filepath+'/'+filename)
        print('reading file: ' + filename)
        for i, row in temp.iterrows():
            print(row[1])
            
