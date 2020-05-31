#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as req
import os
from bs4 import BeautifulSoup

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import Select
from datetime import datetime, timedelta

from selenium.webdriver.chrome.options import Options 
import time
from time import sleep
import requests
import sys
import json
import csv                                                                   
import os.path



chrome_options = Options()  

chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')
chrome_options.add_argument('--Accept-Language=zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3')
chrome_options.add_argument('--Accept=text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

base_dir=os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
web_driver=os.path.join(base_dir,'D:\\chromedriver2.exe')

driver=webdriver.Chrome(executable_path=web_driver,chrome_options=chrome_options)



#Name of csv file:
FileName = 'FileNameOfOutputFile'


######
name = ''
rarity = ''
name = ''
image = ''

day = '1-d'
days7 = '7-d'
month = '1-m'
months3 = '3-m'
months12 =  '12-m'

dates = {
    '1day':day,
    '7days':days7,
    '1month':month,
    '3months':months3,
    '12months':months12
    }



###########

while True:
    if sys.version_info[0] < 3:
        period = str(raw_input('Input time, allowed formats(1day,7days,1month,3months,12months): ')).lower()
        save_period = period
        period = dates[period]

    else:
        period = dates[str(input('Input time, allowed formats(1day,7days,1month,3months,12months): ')).lower()]
        save_period = period
        period = dates[period]
    if sys.version_info[0] < 3:
        geo = str(raw_input('Input geo, allowed formats(GB,US,etc): ')).upper()

    else:
        geo = str(input('Input geo, allowed formats(GB,US,etc): ')).upper()

    if sys.version_info[0] < 3:
        keyword = str(raw_input('Input search keyword: '))
    else:
        keyword = str(input('Input search keyword: '))
        
    if not 'day' in  save_period:       
        baseurl = 'https://trends.google.com/trends/explore?cat=18&date=today%20{}&geo={}&q={}'.format(period,geo,keyword)
    else:
        baseurl = 'https://trends.google.com/trends/explore?cat=18&date=now%20{}&geo={}&q={}'.format(period,geo,keyword)

    driver.get(baseurl)
    print ('Taking Data From Site...')    
    sleep(10)
    src = driver.page_source
    
    soup=BeautifulSoup(src,'html.parser')
    
    try:
        data=soup.find_all('div',{'fe-related-queries fe-atoms-generic-container'})#[1]
        for one in data:
            if 'Related queries' in str(one):
                data = one
                break


        all_results =data.find_all('div',{'label-text'})
        all_elems = []
        
        for x in range(len(all_results)):
            result = all_results[x].text
            all_elems.append(result)
            sleep(3)
            if x == 2:
                break
            
        all_results = '\n'.join(map(str, all_elems))
    except:
        all_results = 'No data'

    data = {
        
        'Time':save_period.encode('utf-8').decode(),
        'Location':geo.encode('utf-8').decode(),
        'Search Keyword':keyword.encode('utf-8').decode(),
        'Results':all_results.encode('utf-8').decode(),

    }


    print ("Writing scraped data to %s.csv"%(FileName))
    filename = '%s.csv'%(FileName)
    file_exists = os.path.isfile(filename)
    if sys.version_info[0] < 3:
        with open(filename, 'ab') as csvFile:
            fieldnames = ["Time","Location","Search Keyword","Results"]
            writer = csv.DictWriter(csvFile,fieldnames = fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
            print ('Adding')
            sleep(1)
            print ('Added Successfully')
            print ('-----------------')            
    
    else:
        with open(filename, 'a') as csvFile:
            fieldnames = ["Time","Location","Search","Results"]
            writer = csv.DictWriter(csvFile,fieldnames = fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
            print ('Adding')
            sleep(1)
            print ('Added Successfully')
            print ('-----------------')            
   
