from flask import Flask, render_template, request, url_for, flash, redirect
import subprocess
import os
import time
from Auction import * 
from AuctionManage import *
from apscheduler.schedulers.background import BackgroundScheduler

# init
app = Flask(__name__)
# SECRET_KEY
app.config['SECRET_KEY'] = ''

messages = []

auctionManager = AuctionManage([])
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(auctionManager.checkAuctions,'interval',minutes=7)
scheduler.start()

# routes
@app.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        link = request.form['link']
        max_bid = float(request.form['max_bid'])
        user = request.form['user']
        passwrd = request.form['passwrd']

        if not link:
            flash('link is required!')
        elif not max_bid:
            flash('max_bid is required!')
        elif not user:
            flash('username is required!')
        elif not passwrd:
            flash('password is required!')
        else:
            messages.append({'link': link, 'max_bid': max_bid, 'user': user, 'passwrd': passwrd})
            auction = Auction(link, max_bid, user, passwrd)
            auctionManager.addAuction(auction)
            return redirect(url_for('home'))

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
   app.run()
