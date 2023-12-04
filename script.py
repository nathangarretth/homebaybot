from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import sys
import argparse
import time
from datetime import date, datetime, timedelta
from Auction import *
import re
from csv import DictReader

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bid",dest ="bid", default = None, help="bid for auction", type=float)
parser.add_argument("-l", "--link",dest ="link", default = None, help="link to ebay listing")
parser.add_argument("-u", "--username",dest ="username", default = None, help="User name")
parser.add_argument("-p", "--password",dest = "password", default = None, help="Password")
parser.add_argument('-f', action='store_true')
args = parser.parse_args()

driver = webdriver.Firefox()

ebayURL = args.link
driver.get(ebayURL)
time.sleep(4)

def get_cookies_values(file):
    with open(file, encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
    return list_of_dicts

cookies = get_cookies_values('cookies.csv')

for i in cookies:
    driver.add_cookie(i)

driver.refresh()
time.sleep(3)

def getExactEndTime():
    exactTime = driver.find_element("xpath", '//span[@class="ux-timer__text ux-timer__text-urgent"]').get_attribute('innerHTML')
    secondsIndex = exactTime.find('s')
    if(secondsIndex > 0):
        seconds = exactTime[secondsIndex-2:secondsIndex]
        seconds = int(seconds)
    minsIndex = exactTime.find('m')
    if(minsIndex > 0):
        mins = exactTime[0:minsIndex]
        mins = int(mins)
        seconds+=(mins * 60)
    print(seconds)
    return seconds

def placeBid():
    driver.find_element(By.ID, 'bidBtn_btn').click()
    time.sleep(3)
    inputBid = driver.find_element("xpath", "//input[contains(@class, 'textbox__control')]")
    inputBid.send_keys(args.bid)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[text()='Bid']").click()
    time.sleep(20)
    driver.refresh()

while(True):
    time.sleep(3)
    if(getExactEndTime() < 10):
        placeBid()
        break