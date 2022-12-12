# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 01:57:24 2022

@author: Samannoy
"""

# This function is used to access the ScrapeWebsite module and 
# use it in a menu driven program by the user

import ScrapeWebsite as SW
import numpy as np
import pandas as pd
import readJSON as rj
import os

os.chdir(r"I:\\Univ of Utah\\Sem 6\\Prog for Engineers\\Project\\JSON Day3")
dict_total={}
dict_total_norm={}
for files in os.listdir():
    try:
        df=rj.readJSON(files) 
        totaldeaths=df.iloc[-1][1]
        totaldeathsnorm=df.iloc[-1][2]
        name=files.split('_')
        country_name_json=name[1]
        country_name=country_name_json[:-5]
        # print(country_name)
        dict_total[country_name]=totaldeaths
        dict_total_norm[country_name]=totaldeathsnorm
    except:
        print(f'\n Error fetching data of {country_name}')
        
dict_total_sorted=sorted(dict_total.items(), key=lambda item: item[1], reverse=True)
# print(dict_total_sorted[0][0])
# print(dict_total_norm['usa'])

c_list=[]
td_list=[]
tdn_list=[]

for i in range(6):
        c_name=dict_total_sorted[i][0]
        c_list.append(dict_total_sorted[i][0])
        td_list.append(dict_total_sorted[i][1])
        tdn_list.append(int(dict_total_norm[c_name]))
        
dataParse={'Country':c_list,'TotalDeaths':td_list,'TotalDeathsNorm':tdn_list}
df2=pd.DataFrame(dataParse)
path='CountryDataTable.json' #change path here
df2.to_json(path,orient='records')


        
        