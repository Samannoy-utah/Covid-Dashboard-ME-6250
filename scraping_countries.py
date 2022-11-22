# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 17:56:23 2022

@author: jankl
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:01:41 2022

@author: jankl
"""

import string
import requests
from bs4 import BeautifulSoup

URL = "https://www.worldometers.info/coronavirus/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="main_table_countries_today")
countries = results.find_all("a", class_="mt_a")
for country in countries:
    print(country.text)
