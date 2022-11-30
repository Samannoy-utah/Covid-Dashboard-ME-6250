# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 00:32:51 2022

@author: SAMANNOY
"""
import pandas as pd
# The function writes a JSON file containing country data for daily and total deaths as passed by the argument

def writeJSON(title,dates,data,country):
    dataParse={'Dates':dates,'Deaths':data}
    df=pd.DataFrame(dataParse)
    path=r'I:\\Univ of Utah\\Sem 6\\Prog for Engineers\\Project\\'+title+'_'+country+'.json' #change path here
    df.to_json(path) 