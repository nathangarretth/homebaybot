from flask import Flask, render_template, request, url_for, flash, redirect


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
        max_bid = request.form['max_bid']
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
            startBot(link, max_bid, user, passwrd)
            return redirect(url_for('home'))

    return render_template('index.html', messages=messages)

def startBot(link, max_bid, user, passwrd):
    flash(f"Sucessfully submitted. checking validity of input")


if __name__ == '__main__':
   app.run()