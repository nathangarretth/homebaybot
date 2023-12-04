from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime, timedelta
import time

class AuctionManage:
    listofAuctions = []

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, listofAuctions):
        self.listofAuctions = listofAuctions

    def addAuction(self, auction):
        self.listofAuctions.append(auction)

    def checkAuctions(self):
        i = 0
        for auction in self.listofAuctions:
            curr_date = datetime.now()
            if(curr_date.year == auction.date.year and curr_date.month == auction.date.month and curr_date.day == auction.date.day):
                check = auction.date - curr_date
                print(check)
                if(check < timedelta(minutes=10)):
                    self.listofAuctions.pop(i)
                    auction.runBot()
            i+=1
    
