# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 22:20:58 2022

@author: Jared & SAMANNOY
"""
# import string
import requests
import re
from bs4 import BeautifulSoup
import writeJSON as wj
import readJSON as rj

country='india'
fileName='I:\\Univ of Utah\\Sem 6\\Prog for Engineers\\Project\\TotalDeaths_india.json'
URL = "https://www.worldometers.info/coronavirus/country/india/"
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
        print(title)
        print(dates)
        print(data)
        wj.writeJSON(title,dates,data,country)  # country name will be used from the loop
        df=rj.readJSON(fileName)   #fileName will be saved as variable later
        print(df.tail())    # Debug purposes, to be removed later
    # if title == "DailyDeaths":
    #     print(title)
    #     print(dates)
    #     print(data)
        
   
