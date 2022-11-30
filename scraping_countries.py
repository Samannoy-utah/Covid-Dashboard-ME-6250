# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:56:23 2022

@author: jankl
"""

import string
import requests
from bs4 import BeautifulSoup

URL = "https://www.worldometers.info/coronavirus/"
page = requests.get(URL)

countryList=[] # List to store the country names
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="main_table_countries_today")
countries = results.find_all("a", class_="mt_a")
for country in countries:
    countryList.append(country.text)
