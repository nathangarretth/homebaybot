from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import argparse
import time
from datetime import date, datetime, timedelta
import re

#bsoup
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }



#get the current bid from ebay
def getCurrentPrice(ebayURL):
    req = requests.get(ebayURL, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    numString = soup.find_all("div", {"class": "x-price-primary"})
    innerhtml = numString[0].text
    num = re.findall(r"[-+]?(?:\d*\.*\d+)", innerhtml)
    num = float(num[0])
    return num


def getEndTime(ebayURL):
    req = requests.get(ebayURL, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    # print(soup.prettify())
    #<span class="ux-timer__time-left">Monday, 03:34 PM</span>
    numString = soup.find_all("span", {"class": "ux-timer__text"})
    innerhtml = numString[0].string
    index_days = innerhtml.find("d")
    index_hours = innerhtml.find("h")
    days = innerhtml[index_days-1:index_days]
    hours = innerhtml[index_hours-2:index_hours]
    days = int(days)
    hours = int(hours)
    end_date = datetime.now() + timedelta(days=days, hours=(hours-1))
    return end_date
    
