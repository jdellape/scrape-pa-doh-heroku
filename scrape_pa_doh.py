#Author: John Dellape
#Date: 4/21/2020

'''
   # Description: This file scrapes https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx which is the
   #              which is the web page that the PA department of health uses for posting daily COVID-19 stats by county.
   #              This file compiles a dataframe composed of the following columns: 
   #                         County Name, State Abbreviation, Confirmed Cumulative Positive Case Count, Confirmed Death Count, Date
   #              This file then writes out the dataframe to a data folder on my local machine which is then uploaded to 
   #              the Google sheets file where data for each day is being stored.
'''


#First, import the libraries we will be using for scraping
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Now, we will scrape https://www.health.pa.gov/topics/disease/Pages/Coronavirus.aspx to get numbers on confirmed cases and deaths in PA by county.
# 
# Changed to this page as of 3/19: https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx
# 
# Logic changed on 4/21 due to additional changes made on the pa website and the fact that all county names are now present on the table at the health.pa.gov coronavirus web page

html_confirmed = urlopen('https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx')
bysc_confirmed = BeautifulSoup(html_confirmed.read(), "lxml")

#Create empty containers for storing column values
counties_with_confirmed_cases = []
confirmed_case_count = []
confirmed_death_count = []

#Isolate the tables on the web page
all_tables = bysc_confirmed.find_all('table')

#Grab the table with the information we want
confirmed_table = all_tables[3]

#isolate the information on counties, confirmed cases and deaths within the table
table_tags = confirmed_table.find_all('td')

#Find the confirmed cases and deaths by county below
col_idx = 1 #For isolating which column I'm iterating through

#First 4 items are just headings, skip past them and iterate through all other rows
for tag in table_tags[4:]:
    item = tag.text.strip()
    #Strip off leading chars for some table items that cause issues
    if item.find("\u200b") != -1:
        item = item.replace("\u200b", "")
    if item.find("\xa0") != -1:
        item = item.replace("\xa0", "")
    #Make additions to apprpriate list
    if col_idx == 1:
        counties_with_confirmed_cases.append(item)
    if col_idx == 2:
        confirmed_case_count.append(item)
    if col_idx == 4:
        confirmed_death_count.append(item)
        col_idx = 0
    #increment my column identifier
    col_idx += 1

#Now, import numpy and pandas for joining all this information into dataframe
import pandas as pd
import datetime

#Create the pandas dataframe
df = pd.DataFrame({'County':counties_with_confirmed_cases,
                   'State': ['PA' for county in counties_with_confirmed_cases],
                   'Cumulative Confirmed Cases': confirmed_case_count,
                   'Cumulative Confirmed Deaths' : confirmed_death_count          
})

df.insert(4, "As of", str(pd.Timestamp.now())[:10]) 


#Import the class from our utility file for writing the df to Google Sheets
from gsheets import GSheetsWriter

workbook_name = "Covid19PA_DEV"
sheet_idx = 0

writer = GSheetsWriter(df, workbook_name)

writer.connect_to_workbook()
writer.write_df_to_sheet(sheet_idx)


