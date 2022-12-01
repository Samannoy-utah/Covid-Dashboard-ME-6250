# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:53:17 2022

@author: Jared and Samannoy
"""

# All imports here
import requests
import re
from bs4 import BeautifulSoup
#import writeJSON as wj
#import readJSON as rj
from tqdm import tqdm

def get_country_list(formatting="list"):    #defaulted to list format
    """
    Retrieve a list of valid countries from Worldometer.
    
    :formatting: a string input, either 'list' or 'URL' are valid
    
    :return: a list, either of country names if 'list' is passed, 
        or the worldometer url format if 'URL' is passed
    """
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
    if formatting == "list":
        return countryList
    elif formatting == "URL":
        return countryURL
    else:
        return "Invalid parameter type"

def get_country_pop(country):
    countryDatabase = get_country_list("list")
    URLDatabase = get_country_list("URL")
    index = countryDatabase.index(country.casefold())
    country_popURL = URLDatabase[index][8:-1]
    URL = "https://www.worldometers.info/world-population/" + country_popURL + "-population/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.find("div", class_="col-md-8 country-pop-description")
    result = str(result)
    start_text = "is <strong>"
    start = result.find(start_text) + len(start_text)
    end_text = "</strong> as"
    end = result.find(end_text)
    population = result[start:end]
    population = population.replace(',','')
    return int(population)
    
def scrape_country(country,website="https://www.worldometers.info/coronavirus/"):
    dailyDeaths = []
    dailyDeathsNormalized = []
    totalDeaths = []
    totalDeathsNormalized = []
    dates = []
    URL = "https://www.worldometers.info/coronavirus/"
    if website != URL:
        return "Website not supported"
    countryDatabase = get_country_list("list")
    URLDatabase = get_country_list("URL")
    if country.casefold() not in countryDatabase:
        return "Country not recognized"
    population = get_country_pop(country)
    index = countryDatabase.index(country.casefold())
    URL = URL + URLDatabase[index]
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
        
        if title == "TotalDeaths" or title == "DailyDeaths":
            start_text = 'xAxis:{categories:["'
            start = graph.find(start_text) + len(start_text)
            end_text = '"]},yAxis'
            end = graph.find(end_text)
            dates = graph[start:end].strip().split('","')   #split to remove the " in the raw data
                
            start_text = "data:["
            start = graph.find(start_text) + len(start_text)
            if 'Daily' in title:
                end_text = "]},{name:"
            else:
                end_text = "]}],responsive"
            end = graph.find(end_text)
            data = graph[start:end].strip().split(",")
            newData = []
            for i in range(len(data)):
                newData.append(data[i].replace(',',''))
                if newData[i] != "null":
                    newData[i] = int(newData[i])
            
            if title == "TotalDeaths":
                totalDeaths = newData
                for deaths in totalDeaths:
                    if deaths == "null":
                        totalDeathsNormalized.append("null")
                    else:
                        totalDeathsNormalized.append(deaths/(population/1000000))
            elif title == "DailyDeaths":
                dailyDeaths = newData
                for deaths in dailyDeaths:
                    if deaths == "null":
                        dailyDeathsNormalized.append("null")
                    else:
                        dailyDeathsNormalized.append(deaths/(population/1000000))
        
    print(dates)
    print(totalDeaths)
    print(totalDeathsNormalized)
    print(dailyDeaths)
    print(dailyDeathsNormalized)

def scrape_countries(countryList):
    countryDatabase = get_country_list("list")
    URLDatabase = get_country_list("URL")
    indices = []
    for i in len(countryList):
        if countryList[i] in countryDatabase:
            indices.append(countryList.index(countryList[i]))
    for i in tqdm(indices):
        URL='https://www.worldometers.info/coronavirus/'+URLDatabase[i]
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
            dates = graph[start:end].strip().split('","')   #split to remove the " in the raw data
                
            start_text = "data:["
            start = graph.find(start_text) + len(start_text)
            if 'Daily' in title:
                end_text = "]},{name:"
            else:
                end_text = "]}],responsive"
            end = graph.find(end_text)
            data = graph[start:end].strip().split(",")
            
            #if title == "TotalDeaths":
                # fileName variable kept for debugging the readJSON function
                #fileName='I:\\Univ of Utah\\Sem 6\\Prog for Engineers\\Project\\JSON\\'+title+'_'+countryList[i]+'.json'
                # print(title)
                # print(dates)
                # print(data)
                #wj.writeJSON(title,dates,data,countryList[i])  # country name will be used from the loop
                #df=rj.readJSON(fileName)   #fileName will be saved as variable later
                #print("\n") # Debug purposes, to be removed later
                #print(countryList[i]) # Debug purposes, to be removed later
                #print(df.tail())    # Debug purposes, to be removed later
                
            # if title == "DailyDeaths":
            #     # print(title)
            #     # print(dates)
            #     # print(data)
            #     wj.writeJSON(title,dates,data,countryList[i])
    
scrape_country("USA")