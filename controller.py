#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

import orm, model, wrapper

connection = sqlite3.connect('db/stocktrade.db')
cursor = connection.cursor()

@app.route('/')
def index():
    h1 = 'Home'
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

@app.route('/lookup', methods = ["GET","POST"])
def lookup():
    h1 = 'Symbol Look Up'
    title = 'Terminal Trader'
    data = request.form['name']
    payload_from_wrapper = wrapper.get_company_info(data)
    name,exchange,symbol = payload_from_wrapper
    return render_template('lookup.html',h1=h1,title=title, name=name,exchange=exchange,symbol=symbol)

@app.route('/getstockprice', methods = ["GET","POST"])
def getstockprice():
    h1 = 'Get Stock Price'
    title = 'Terminal Trader'
    data = request.form['name']
    payload_from_wrapper = wrapper.get_stock_price(data)
    name, price = payload_from_wrapper
    return render_template('getstockprice.html',h1=h1,title=title,name=name,price=price)

if __name__ == '__main__':
    app.run(debug=True)
