# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:53:17 2022
@author: Jared and Samannoy
"""

# All imports here
import requests
import re
from bs4 import BeautifulSoup
import writeJSON as wj
from tqdm import tqdm  # Just to keep track of the progress of the running code
import datetime

# All function definitions here

##############################################################################
# The function fetches the list of all countries from the worldometer website
# The function can also fetch the list of URL of individual country pages

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




##############################################################################
# The function returns the population data of the country passed as argument

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
    


##############################################################################
# The function scrapes data from the website and for the country passed as argument
# The writeJSON is a custom function that generates the JSON file and save with
# today's date and country's name

def scrape_country(country,website="https://www.worldometers.info/coronavirus/"):
    dailyDeaths = []
    dailyDeathsNormalized = []
    totalDeaths = []
    totalDeathsNormalized = []
    dates = []
    today=str(datetime.datetime.now().date())
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

    #print here for debug purposes        
    # print(dates)
    # print(totalDeaths)
    # print(totalDeathsNormalized)
    # print(dailyDeaths)
    # print(dailyDeathsNormalized)
    wj.writeJSON(today,dates,totalDeaths,totalDeathsNormalized,dailyDeaths,dailyDeathsNormalized,country)


##############################################################################    
# The function utilizes the list of all countries found on the website and
# uses the scrape-country function to loop over all countries and scrape all data
               
def scrape_countries(website="https://www.worldometers.info/coronavirus/"):
    
    URL = "https://www.worldometers.info/coronavirus/"
    if website != URL:
        return "Website not supported"
    countryDatabase = get_country_list("list")
    URLDatabase = get_country_list("URL")    
    for i in tqdm(range(len(URLDatabase))):
        country=countryDatabase[i]
        try:
            scrape_country(country)
        except:
            print(f'\n Error fetching data of {country}')



##############################################################################
## Implementing the functions to test
# The below code is commented out as this module is being used in the main.py

# scrape_country("USA")   # Single country data scraping
# scrape_countries()      # All country data scraping at once
