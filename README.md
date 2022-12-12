# Covid-Dashboard-ME-6250
Covid Dashboard project for ME 6250 Fall 2022

- [x] Part 1

## Instructions to run the code: <br>

**Run the main.py from an IDE or from command line and follow the menu-driven instructions on the terminal to fetch data from one or all countries** <br>
*Libraries imported: requests, re,bs4,tqdm,datetime,pandas*

* The **ScrapeWebsite.py** file is used as the data scraping module that has all included functions and implementations. <br>
  * It includes the function named **scrape_country** which takes in 2 arguments- country and optional website URL (However, the current version of the code works only with the worldometer website)
  * Specifically, **scrape_country** finds all of the instances of scripts with type "text/javascript" to narrow down to the charts on the country-specific page, removes the whitespace, and searches for the known starting and ending keywords for desired information. From there, daily death information and cumulative death information are extracted from their respective graphs.
  * We desired to use multiple data sources, however we struggled to find others that could be statically scraped for daily and cumulative data for each day of the pandemic. For instance, NYT, health.google.com, ourworldindata.org, and covid19.who.int all required dynamic web scraping which we did not attempt. Additionally, sites like covid19.who.int and Johns Hopkins have static, accessible data but that data is only present-day data and cannot show the individual day data throughout the pandemic as desired. Also, some of these sources already provide the JSON file, which does not serve the purpose of web scraping.
* The **writeJSON.py** file is a custom code that utilizes Pandas library to prepare the JSON file from the scraped data and generates the JSON file with the passed arguments. <br>
  * The function prepares the JSON file with the data in the following order: Date, TotalDeaths,TotalDeathsNormalized, DailyDeaths, DailyDeathsNormalized
  * The data is then saved as **(date_of_scraping)_(countryname).JSON**
* The **main.py** file is a menu driven program for the user to run:
  * It runs a continuous loop asking the user to enter 1 to scrape one country, 2 to scrape all countries or 0 to exit
  



### Challenges faced: ###
1. The country data url needs to be customized for different countries: <br>
For eg: <A> https://www.worldometers.info/coronavirus/country/india/<br>
<B> USA: https://www.worldometers.info/coronavirus/country/us/<br>
<C> Isle of Man: https://www.worldometers.info/coronavirus/country/isle-of-man/<br>

*Fix:* This issue is fixed by fetching href tags of each country name and storing all country specific URLs in a separate list

2. Not all the 228 countries on the Worldometer website has death data/plots, so we are unable to fetch those data. Also, the population data of all countries are not updated in the specific tag that displays live population count.

This was crashing and exiting the code as soon as the error was found.

*Fix:* Exception handling has been implemented with try except statements that throws an error message when the code faces any issue and mentions the country name that faced the issue.


- [ ] Part 2

## Instructions to run the code: <br>

**Download the zip file in folder 'Part 2'. All the required py files and dependent modules are inside the same folder. 
Run the pytoHTML.py from an IDE or from command line and it should automatically generate the HTML file named 'CovidDashboard_Samannoy_Jared' inside the HTML folder. Open the HTML file in a browser to test the features** <br>

*Do not delete the assets or jquery folder from inside HTML as it contains all the necessary css files*

* The **pytoHTML.py** file is the main py file to call all plotting functions (Single_country_plotter, Multi_country_plotter)  <br>
 * The code generates all the scripts and div tags of each plot by using the 'components' functionality of Bokeh
 * These script and div tags are processed as required and attached in specific div tags of the semi prepared HTML code
 * After embedding all necessary scripts and div tags, the final HTML file is generated and stored
