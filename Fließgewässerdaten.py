#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:51:56 2022

@author: lyth
"""

import json
import requests
from matplotlib import pyplot as plt
import datetime 
import time
import matplotlib.dates as md 
import argparse

def arguments_parser():
	parser = argparse.ArgumentParser(description="This graphs data about water quality in wendlingen")
	parser.add_argument('-d','--days',default = 365*3, type=int,help="number of days to fetch data from ending with latest data point. default is set to three years. minimum is one day")
	
	return parser.parse_args()
		
args = arguments_parser()
days = args.days

dt = 3600000*24*days
t0 = int(time.time()*1000) # current time
t1 = t0 -dt # how far back you want to go

leb = ['temp','o2','ph','lf','tr']
url = 'https://lupo-cloud.de/water/metric/de.lubw.gewaesser.'
data=[]

for i in leb:
    res = requests.get(url+i+'?labels=station:2875&from='+str(t1)+'&to='+str(t0))
    data.append(json.loads(res.text))

fig,ax =plt.subplots(len(leb),sharex=True)
fig.suptitle('Fließgewässerdaten Wendlingen \n letzte Datenpunkt  '+str(datetime.datetime.fromtimestamp(data[0][-1]['times'][-1]/1000)))    
xfmt = md.DateFormatter('%m-%d')#'%H:%M')
ax[-1].xaxis.set_major_formatter(xfmt)

C = ['r','b','g','y','k']
E = ['°c','[mg/l]','pH',r'$\mu$ S/cm','[FNU]']
L = ['Temp.','o2','pH','Leitf.','Trüb.' ]

for i,j,c,e in zip(range(len(leb)),L,C,E):
    ax[i].plot([datetime.datetime.fromtimestamp(k/1000) for k in data[i][-1]['times']],data[i][-1]['values'],c,label=j)
    ax[i].legend(loc=2)
    ax[i].set_ylabel(e)
    
print('last data point', datetime.datetime.fromtimestamp(data[3][-1]['times'][-1]/1000))

plt.show()
