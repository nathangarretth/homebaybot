from flask import Flask, render_template, request, url_for, flash, redirect
import subprocess
import os
from functions import *


# init
app = Flask(__name__)
# SECRET_KEY here
# app.config['SECRET_KEY'] = ''

messages = []


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
            checkValidity(link, max_bid, user, passwrd)
            return redirect(url_for('home'))

    return render_template('index.html', messages=messages)

def checkValidity(link, max_bid, user, passwrd):
    flash(f"Sucessfully submitted. checking validity of input")
    saveLink(link)
    time.sleep(1)
    scrapeValid = scrapeValidity(link, max_bid, user, passwrd)
    if(scrapeValid[0]):
        flash("input is valid")
        time.sleep(1)
        runBot(link, max_bid, user, passwrd)
    else:
        flash(f"input not valid: {scrapeValid[1]}")

def saveLink(link):
    if(os.path.exists('data.txt')):
        f = open("filename", "w")
        f.write(link)
        f.close()
    else:
        f = open("data.txt", "x")
        f.write(link)
        f.close()


def scrapeValidity(link, max_bid, user, passwrd):
    if("Auction=1" not in link):
        return False, "not auction"
    elif(max_bid < getCurrentPrice(link)):
        return False, "your bid is lower than current bid"
    else:
        return True, "sucess"

def runBot(link, max_bid, user, passwrd):
    currDir = os.getcwd()
    #subprocess.call(['gnome-terminal', '--'])

    subprocess.call(['gnome-terminal', '-x', "python3", "script.py", "-f", "-b", f"{max_bid}", "-u", f"{user}", "-p", f"{passwrd}"])
    flash("Bot has started up!! You can now leave the page.")
    



if __name__ == '__main__':
   app.run()
