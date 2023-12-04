from flask import Flask, render_template, request, url_for, flash, redirect
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import subprocess
from sys import platform
from datetime import date, datetime, timedelta
import time
import os

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

class Auction:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, link, max_bid, user, passwrd):
        self.link = link
        self.max_bid = max_bid
        self.user = user
        self.passwrd = passwrd
        self.date = self.getEndTime(link, True)
    
    def checkValidity():
        flash(f"Sucessfully submitted. checking validity of input")
        time.sleep(1)
        scrapeValid = scrapeValidity()
        if(scrapeValid[0]):
            flash("input is valid")
            time.sleep(1)
            runBot()
        else:
            flash(f"input not valid: {scrapeValid[1]}")

    def scrapeValidity():
        if("Auction=1" not in link):
            return False, "not auction"
        elif(max_bid < getCurrentPrice(self.link)):
            return False, "your bid is lower than current bid"
        else:
            return True, "sucess"

    def getCurrentPrice(ebayURL):
        req = requests.get(ebayURL, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        numString = soup.find_all("div", {"class": "x-price-primary"})
        innerhtml = numString[0].text
        num = re.findall(r"[-+]?(?:\d*\.*\d+)", innerhtml)
        num = float(num[0])
        return num
    
    # scraping auction endtime w/ selenium
    def getEndTime(self, ebayURL, fire):
        driver = webdriver.Firefox()
        
        driver.get(ebayURL)
        time.sleep(4)
        exactTimeElement = driver.find_element("xpath", '//span[@class="ux-timer__time-left"]')
        exactTime = exactTimeElement.get_attribute('innerHTML')
        commaIndex = exactTime.find(',')
        if(commaIndex > 0):
            day = exactTime[0:commaIndex]
            timeString = exactTime[commaIndex+1:len(exactTime)]
            endDay = time.strptime(day, "%A").tm_wday
            today = date.today().weekday()
            addDays = (7-today) + endDay
            timeString = exactTime[commaIndex+1:len(exactTime)]
        else:
            addDays = 0
            timeString = exactTime[6:len(exactTime)]
        finalTime = self.convert24(timeString)
        current_date = date.today()
        finalDate = current_date + timedelta(days=addDays)
        finalFinalDate = datetime(finalDate.year, finalDate.month, finalDate.day, finalTime.hour, finalTime.minute)
        driver.quit()
        print(finalFinalDate)
        return finalFinalDate

    def convert24(self, time):
        t = datetime.strptime(time, '%I:%M %p')
        return t

    def runBot(self):
        subprocess.call(['gnome-terminal', '--', "python3", "script.py", "-f", "-b", f"{self.max_bid}", "-u", f"{self.user}", "-p", f"{self.passwrd}", "-l", f"{self.link}"])
    
