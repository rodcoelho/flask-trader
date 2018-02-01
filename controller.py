#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)

import sqlite3

import orm, wrapper

connection = sqlite3.connect('db/stocktrade.db')
cursor = connection.cursor()

@app.route('/')
def index():
    h1 = 'Home'
    title = 'Terminal Trader'
    return render_template('index.html',h1=h1,title=title)

@app.route('/portfolio',methods = ["GET","POST"])
def portfolio():
    h1 = 'Portfolio'
    title = 'Terminal Trader'
    username = 'rodrigo'
    cash = orm.get_balance(username)
    stocks_in_portfolio = orm.sell_get_list_of_positions(username)
    if stocks_in_portfolio is not False:
        current_prices = {}
        # [ (ticker, price, quantity ) ]
        for stocks in stocks_in_portfolio:
            name, price = wrapper.get_stock_price(stocks[0])
            current_prices[stocks[0]] = price
        NPV = 0
        for stocks in stocks_in_portfolio:
            stock_q_times_p = float(stocks[2]) * float(current_prices[stocks[0]])
            NPV += stock_q_times_p
        stock_payload = [[x[0], x[2]] for x in stocks_in_portfolio]
        NPV += float(cash)
        NPVreturn = (NPV - 1000000.0) / 1000000.0
        if NPVreturn > 0.999999:
            NPVmessage = 'up'
        else:
            NPVmessage = 'down'
        #clean up data
        cash ='{:.2f}'.format(cash)
        NPV = '{:.2f}'.format(NPV)
        NPVreturn = '{:.6f}'.format(NPVreturn)
        return render_template('portfolio.html',h1=h1,title=title,cash=cash,
                               NPV=NPV,NPVreturn=NPVreturn, up_or_down=NPVmessage, stocks=stock_payload)
    return render_template('error.html', h1=h1, title=title, error_message='Portfolio Error')


@app.route('/buy',methods = ["GET","POST"])
def buy():
    h1 = 'Buy'
    title = 'Terminal Trader'
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    # get price
    payload_from_wrapper = wrapper.get_stock_price(symbol)
    price = payload_from_wrapper[1]
    if price is not None:
        # check if person can buy quantity
        cost = float(price) * float(quantity)
        username = 'rodrigo'
        cash_balance = orm.get_balance(username)
        print(cash_balance,cost)
        if cash_balance > cost:
            #if they can buy quantity, subtract cost from balance
            payload_message1 = orm.buy_stocks_users_table(username,cost, cash_balance)
            if payload_message1 is True:
                # add to positions table and transactions table
                orm.buy_stocks_positions_table(quantity,symbol,price,username)
                payload_message2=orm.buy_stocks_transactions_table(quantity,symbol,price,username)
                if payload_message2 is True:
                    # return success confirmation
                    return render_template('buy.html', h1=h1, title=title, quantity=quantity,symbol=symbol,price=price)
                else:
                    return render_template('error.html', h1=h1, title=title,
                                           error_message="Error at positions or transactions table")
            else:
                return render_template('error.html', h1=h1, title=title,
                                       error_message="Error at users table")
        else:
            # else return to error.html with error message
            return render_template('error.html', h1=h1, title=title,
                                   error_message="You don't have enough cash to make this transaction")
    else:
        return render_template('error.html', h1=h1, title=title, error_message="Stock does not exist")


@app.route('/sell',methods=["GET","POST"])
def sell():
    h1 = 'Sell'
    title = 'Terminal Trader'
    symbol = request.form['symbol']
    quantity = request.form['quantity']
    username = 'rodrigo'
    # get price
    payload_from_wrapper = wrapper.get_stock_price(symbol)
    price = payload_from_wrapper[1]
    if price is not None:
        # check if person has shares to sell... list_of_positions =  [ (ticker, price, quantity ) ]
        list_of_positions = orm.sell_get_list_of_positions(username)
        for _ in list_of_positions:
            if _[0] == symbol:
                list_of_positions= _
        if len(list_of_positions) != 0:
            if int(list_of_positions[2]) >= int(quantity):
                # edit users table
                income = float(price) * float(quantity)
                payload_message1, new_balance, income = orm.sell_stocks_user_table(username,income)
                if payload_message1 is not False:
                    # edit transactions table
                    payload_message2 = orm.sell_stocks_transactions_table(username,symbol,quantity,price)
                    if payload_message2 is not False:
                        # edit positions table
                        orm.sell_stocks_positions_table(username,symbol,float(quantity),float(price))
                        return render_template('sell.html',h1=h1,title=title,symbol=symbol,
                                               quantity=quantity,price=price,income=income, new_balance=new_balance)
                    else:
                        return render_template('error.html', h1=h1, title=title,
                                               error_message='Error at transactions table')
                else:
                    return render_template('error.html', h1=h1, title=title,
                                           error_message='Error at users table')
            else:
                return render_template('error.html', h1=h1, title=title, error_message='You do not own enough shares')
        else:
            return render_template('error.html', h1=h1, title=title, error_message='You do not own this stock')
    else:
        return render_template('error.html', h1=h1,title=title,error_message='Stock symbol does not exist')

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
    symbol = request.form['symbol']
    payload_from_wrapper = wrapper.get_stock_price(symbol)
    name, price = payload_from_wrapper
    return render_template('getstockprice.html',h1=h1,title=title,name=name,price=price)

if __name__ == '__main__':
    app.run(debug=True)
