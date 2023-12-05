# homebaybot

## About The Project

This project is a bot for homelabs to snipe ebay listings in the last few seconds. Ebay does have a built-in feature similar to this, but automatic bidding will increase the price on your behalf when someone else increases the bid. This project just aims to conceal your highest price until the last second.

## info

This project is being tested on ubuntu 22.04.3. It uses flask to get auction details (the link to the auction, your max bid) and then schedules the ebay bot to login using cookies and place the bid a few seconds before the auction ends.

## setup

1. clone repo
   ```sh
   git clone https://github.com/nathangarretth/homebaybot.git
   ```
2. install from the requirements file
   ```sh
   pip install -r requirements.txt
   ```
3. copy ebay cookies into cookies.csv
4. setup flask on vm
