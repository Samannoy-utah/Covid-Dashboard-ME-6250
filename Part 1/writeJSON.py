# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 00:32:51 2022

@author: Samannoy
"""
import pandas as pd
# The function writes a JSON file containing country data for 
# daily and total deaths as passed by the argument

def writeJSON(title,dates,data1,data2,data3,data4,country):
    dataParse={'Dates':dates,'TotalDeaths':data1,'TotalDeathsNormalized':data2,'DailyDeaths':data3,'DailyDeathsNormalized':data4}
    df=pd.DataFrame(dataParse)
    path=title+'_'+country+'.json' #change path here
    df.to_json(path) 
