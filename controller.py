#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)

import sqlite3

import orm, model

connection = sqlite3.connect('db/stocktrade.db')
cursor = connection.cursor()

@app.route('/')
def index():
    h1 = 'Terminal Trader'
    title = 'Terminal Trader'
    return render_template('index.html',h1=h1,title=title)

@app.route('/portfolio')
def portfolio():
    h1 = 'Portfolio'
    title = 'Terminal Trader'
    return render_template('portfolio.html',h1=h1,title=title)

@app.route('/buy')
def buy():
    h1 = 'Buy'
    title = 'Terminal Trader'
    return render_template('buy.html',h1=h1,title=title)

@app.route('/sell')
def sell():
    h1 = 'Sell'
    title = 'Terminal Trader'
    return render_template('sell.html',h1=h1,title=title)

@app.route('/lookup')
def lookup():
    h1 = 'Symbol Look Up'
    title = 'Terminal Trader'
    return render_template('lookup.html',h1=h1,title=title)

@app.route('/getstockprice')
def getstockprice():
    h1 = 'Get Stock Price'
    title = 'Terminal Trader'
    return render_template('getstockprice.html',h1=h1,title=title)

if __name__ == '__main__':
    app.run(debug=True)
