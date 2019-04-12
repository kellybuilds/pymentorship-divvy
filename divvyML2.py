# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 09:40:41 2019

@author: Kelly
divvy_ML
"""
import sklearn
import statsmodels
import statsmodels.api as sm
from sklearn import datasets
import matplotlib.pyplot as plt
import seaborn as sns

#focus on one station for now... find out which station has the most rides (from_station_id)
testdf1.from_station_name.nunique()
testdf1.from_station_id.nunique()
    #why is there a different number for name and id? Maybe they changed the names over the two years?
testdf1['from_station_id'].value_counts()
    #station id 35 has the most rides with "from"; that station is "Streeter Dr & Grand Ave"

#make train and valid dfs with only station id 35
testdf35 = testdf1.loc[testdf1['from_station_id'] == 35]
testdf35.reset_index(drop=True, inplace=True)   #resets index
#visualize numeric data
testdf35[testdf35.dtypes[(testdf35.dtypes=="float64")|(testdf35.dtypes=="int64")]
            .index.values].hist(figsize=[11,11])

#for now, keep only day (of the week), month, and season
testdf35 = testdf35[['day',
                     'month',
                     'season',
                     'date']].copy()

#extra preprocessing step... I need a target variable - count for each day, keep day, month, and season cols
testdf35 = testdf35.groupby(['date', 
                             'day', 
                             'month', 
                             'season'])['date'].count().to_frame('count').reset_index()

#time series with dates over the three years and counts
plt.plot(testdf35['date'], testdf35['count'])

#separate out a testing dataset and validation dataset (years 2016 and 2017)
split_date = datetime.date(2017,12,31)    #split date assigned
df_train = testdf35.loc[testdf35['date'] <= split_date]
df_valid = testdf35.loc[testdf35['date'] > split_date]

#look at relationship between target (count) and dependent features (day, month, season)
daysandcount = df_train.pivot(index='date', 
                              columns='day', 
                              values='count')
daysandcount.boxplot()

monthsandcount = df_train.pivot(index='date', 
                                columns='month', 
                                values='count')
monthsandcount.boxplot()

seasonandcount = df_train.pivot(index='date', 
                                columns='season', 
                                values='count')
seasonandcount.boxplot()


#visualize relationship between features and response using scatterplot
sns.pairplot(df_train, x_vars=['day', 
                               'month', 
                               'season'], y_vars='count', size=7, aspect=0.7, kind='reg')

#linear regression
#preparing x and y - https://www.ritchieng.com/machine-learning-linear-regression/
xtrain = df_train[['day', 'month', 'season']]
ytrain = df_train[['count']]

xtest = df_valid[['day', 'month', 'season']]
ytest = df_valid[['count']]



# import model
from sklearn.linear_model import LinearRegression

# instantiate
linreg = LinearRegression()

# fit the model to the training data (learn the coefficients)
linreg.fit(xtrain, ytrain)

# print the intercept and coefficients
print(linreg.intercept_)
print(linreg.coef_)

#making predictions on the testing set
y_pred = linreg.predict(xtest)



