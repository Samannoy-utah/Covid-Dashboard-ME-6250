# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 01:57:24 2022

@author: Samannoy
"""

# This function is used to access the ScrapeWebsite module and 
# use it in a menu driven program by the user

import ScrapeWebsite as SW

while(True):
    print("\nEnter 1 for single country data scraping")
    print("Enter 2 for all countries data scraping")
    print("Enter 0 to exit loop")
    a=input()
    try:
        if(int(a)==1):
            c=input("Enter the country to scrape data: \n")
            SW.scrape_country(c)
            print(f'Data scraped for {c} and JSON file stored')
            break
        elif(int(a)==2):
            SW.scrape_countries()
            print("Data scraped for all countries and JSON files stored")
            break
        elif(int(a)==0):
            print("Thank you! Exiting loop")
            break
        else:
            print("Invalid input! Enter again")
    except:
        print("Invalid input. Only enter integers")
        
        