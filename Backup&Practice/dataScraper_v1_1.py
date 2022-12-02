# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 01:16:19 2022

@author: Jared & SAMANNOY
"""

# All imports here
import requests
import re
from bs4 import BeautifulSoup
import writeJSON as wj
import readJSON as rj
from tqdm import tqdm

# URL info and declarations
URL = "https://www.worldometers.info/coronavirus/"
page = requests.get(URL)
countryList=[] # List to store the country names
countryURL=[]  # List to store the individual country URL
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="main_table_countries_today")
countries = results.find_all("a", class_="mt_a")
for country in countries:
    countryList.append(country.text.casefold()) #country list prepared here
    countryURL.append(country.attrs["href"]) #country URL list prepared here
# print(countryURL)   # Debug url of each country, different from countryList containing names

for i in tqdm(range(len(countryURL))):
    URL='https://www.worldometers.info/coronavirus/'+countryURL[i]
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")        
    graphs = soup.find_all("script", type="text/javascript")
    for graph in graphs:
        graph = str(graph)
        graph = re.sub(r"\s","",graph)
        start_text = "title:{text:'"
        start = graph.find(start_text) + len(start_text)
        end_text = "'},subtitle:"
        end = graph.find(end_text)
        title = graph[start:end]
            
        start_text = 'xAxis:{categories:["'
        start = graph.find(start_text) + len(start_text)
        end_text = '"]},yAxis'
        end = graph.find(end_text)
        dates = graph[start:end].strip().split('","')
            
        start_text = "data:["
        start = graph.find(start_text) + len(start_text)
        if 'Daily' in title:
            end_text = "]},{name:"
        else:
            end_text = "]}],responsive"
        end = graph.find(end_text)
        data = graph[start:end].strip().split(",")
        
        if title == "TotalDeaths":
            # fileName variable kept for debugging the readJSON function
            fileName='I:\\Univ of Utah\\Sem 6\\Prog for Engineers\\Project\\JSON\\'+title+'_'+countryList[i]+'.json'
            # print(title)
            # print(dates)
            # print(data)
            wj.writeJSON(title,dates,data,countryList[i])  # country name will be used from the loop
            df=rj.readJSON(fileName)   #fileName will be saved as variable later
            print("\n") # Debug purposes, to be removed later
            print(countryList[i]) # Debug purposes, to be removed later
            print(df.tail())    # Debug purposes, to be removed later
            
        # if title == "DailyDeaths":
        #     # print(title)
        #     # print(dates)
        #     # print(data)
        #     wj.writeJSON(title,dates,data,countryList[i])