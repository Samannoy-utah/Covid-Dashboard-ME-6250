# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 00:29:30 2022

@author: SAMANNOY
"""
import pandas as pd
import ScrapeWebsite as SW
import json


countries=SW.get_country_list()
# dictionary={}
# for i in range(len(countries)):
#     # dictionary = {
#     #     "ID": i,
#     #     "country": countries[i],
#     #     }
#     dictionary[i]=countries[i]
# print(dictionary)

# json_string = json.dumps(dictionary)
# print(json_string)
# with open("sample.json", "w") as outfile:
#     outfile.write(json_string)
    
# print(dictionary)
ids=[]
for i in range(len(countries)):
    ids.append(int(i))
dataParse={'ID':ids,'Countries':countries}
df=pd.DataFrame(dataParse)
path='CountryList.json' #change path here
df.to_json(path,orient='records') 