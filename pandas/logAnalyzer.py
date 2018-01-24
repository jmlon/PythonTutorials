#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Read an apache log file into a Pandas Dataframe.
Analyze the data, produce graphs for the analysis.

Author: Jorge Londoño
Date:   2018-01-12
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil.parser import *


def apacheDateParser(x,y):
    '''Parses a string into a datetime object'''
    return parse(x+' '+y, fuzzy=True)    


def myIntParser(x):
    '''Converts a string into an integer, otherwise return NaN'''
    try:
        # Throws a ValueError exception if is not a valid integer
        return int(x)
    except ValueError:
        return np.nan


data = pd.read_csv('access_log', encoding='iso-8859-1',
    delim_whitespace=True, 
    header=None, 
    parse_dates={ 'dt': [3,4] },
    date_parser=apacheDateParser,
    index_col=0, 
    names=['client','id','user','datetime','tz','request','status','size','referer','agent'],
    converters={ 'status':myIntParser, 'size': myIntParser },
    dtype={ 'referer': object, 'agent': object } )
    
print(data.shape)

print(data.head())

print(data.dtypes)

print(data['size'].mean())

print(data['size'].std())

print(data['size'][data['size'].isnull()].head())

print(data['size'].count())

grpHitsWDay = data[['id']].groupby(data.index.weekday, sort=False)
print(grpHitsWDay)
print(grpHitsWDay.indices)
print(grpHitsWDay.count())

hits = grpHitsWDay.count()
hits.index = [ 'Mon','Tue','Wed','Thu','Fri','Sat','Sun' ]
hits.columns = [ 'Hits' ]
print(hits)

print(hits.describe())

hits.plot(kind='bar', figsize=(8,6), colormap='summer', title='Hits per weekday', legend=False)
plt.show()

grpWDay = data[ ['id','size'] ].groupby(data.index.weekday)
stats = grpWDay.aggregate({ 'id':lambda x: x.count(), 'size':np.sum })
print(stats)

stats = grpWDay.aggregate({ 'id':lambda x: x.count(), 'size':np.sum }).rename(columns={'size':'Bytes', 'id':'Hits'})
stats.index=[ 'Mon','Tue','Wed','Thu','Fri','Sat','Sun' ]
print(stats)

stats.plot(kind='bar', figsize=(8,6), colormap='summer', title='Hits & bytes per weekday', subplots=True)
plt.show()    

print(data['request'].head(10))

data['resource'] = data['request'].apply(lambda x: x.split()[1])
print(data['resource'].head(10))

grpRsc = data[ ['id','size'] ].groupby(data['resource'])
stats = grpRsc.aggregate({ 'id':lambda x: x.count(), 'size':np.sum }).rename(columns={'size':'XferBytes', 'id':'Hits'})
print(stats)

sortedh = stats.sort_values(by='Hits', ascending=False)
print(sortedh.head(10))

sortedb = stats.sort_values(by='XferBytes', ascending=False)
print(sortedb.head(10))

sortedb.head(10).plot(kind='bar', figsize=(8,5), colormap='summer', title='Xfer & Hits (sorted by Xfer)', subplots=True)
plt.show()












