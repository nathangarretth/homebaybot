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
from datetime import date, datetime
from functions import *
import re

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bid",dest ="bid", default = None, help="bid for auction", type=float)
parser.add_argument("-u", "--username",dest ="username", default = None, help="User name")
parser.add_argument("-p", "--password",dest = "password", default = None, help="Password")
parser.add_argument('-f', action='store_true')
args = parser.parse_args()

#bot code


# set webdriver
if(args.f):
    driver = webdriver.Firefox()
else:
    chromeDriver = ''
    if platform == "linux" or platform == "linux2":
        chromeDriver = 'chromedriver'
    elif platform == "win32":
        chromeDriver = 'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    ser = Service(chromeDriver)
    driver = webdriver.Chrome(service=ser, options=chrome_options)


# get url
with open('data.txt', 'r') as file:
    ebayURL = file.read().replace('\n', '')

driver.get(ebayURL)
time.sleep(3)

#login
#user
driver.find_element(By.XPATH, "//*[text()='Sign in']").click()
time.sleep(3)
username = driver.find_element(By.ID, 'userid')
username.send_keys(args.username)
driver.find_element(By.ID, 'signin-continue-btn').click()
time.sleep(3)
#pass
passwrd = driver.find_element(By.ID, 'pass')
passwrd.send_keys(args.password)
driver.find_element(By.ID, 'sgnBt').click()
time.sleep(3)


# place bid
driver.find_element(By.ID, 'bidBtn_btn').click()
time.sleep(3)
inputBid = driver.find_element(By.XPATH, "//input[contains(@class, 'textbox__control')]")
inputBid.send_keys(args.bid)

time.sleep(50)


    

