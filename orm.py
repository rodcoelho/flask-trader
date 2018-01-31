import sqlite3
import datetime

connection = sqlite3.connect('db/stocktrade.db')
cursor = connection.cursor()

def register(username,password):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
INSERT INTO users(name, password, balance)
VALUES ('{}','{}',100000);
    """.format(username,password))
        connection.commit()
        return True
    except:
        connection.commit()
        return False

def login(username,password):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
    SELECT name, balance
    FROM users
    WHERE name = '{}' AND password = '{}';
        """.format(username, password))
        fetch = cursor.fetchall()
        try:
            connection.commit()
            return True, fetch[0][0], fetch[0][1]
        except:
            connection.commit()
            return False, False, False
    except:
        connection.commit()
        return False, False, False

def get_balance(username):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        SELECT balance
        FROM users
        WHERE name = '{}'
        ;
            """.format(username))
        fetch = cursor.fetchone()
        connection.commit()
        return fetch[0]
    except:
        connection.commit()
        return False

def buy_stocks_users_table(username,cost, cash_balance):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # update the balance in the USERS table to show that he bought shares
    difference = float(cash_balance) - float(cost)

    try:
        cursor.execute("""
            UPDATE users SET balance = '{}' WHERE name = '{}'
            ;
                """.format(difference, username))
        connection.commit()
        return True
    except:
        connection.commit()
        return False

def buy_stocks_transactions_table(quantity,ticker,price,username):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
        SELECT pk FROM users WHERE name = '{}'
                    ;
                        """.format(username))
    id = cursor.fetchone()
    now = datetime.datetime.now()

    # update the TRANSACTIONS table to show that he bought shares
    try:
        cursor.execute("""
                INSERT INTO transactions(userID, symbol, unixtime, lastprice, quantity, buysell)
                VALUES ('{}','{}','{}','{}','{}','{}')
                ;
                    """.format(id[0],ticker,now,price, quantity,'b' ))
        connection.commit()
        return True
    except:
        connection.commit()
        return False

def buy_stocks_positions_table(quantity,ticker,price,username):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
            SELECT pk FROM users WHERE name = '{}'
                        ;
                            """.format(username))
    id = cursor.fetchone()

    # check if anything in positions exists. If so create VWAP and then UPDATE. Else add to positions.
    cursor.execute("""
            SELECT VWAP, quantity
            FROM positions
            WHERE userID = '{}' AND symbol = '{}';
                        """.format(id[0], ticker))
    VWAP_query = cursor.fetchall()

    # if VWAP doesn't exist in positions list then add to positions
    if len(VWAP_query) == 0:
        # check if initial commit of symbol to position - if so we can add to position'
        cursor.execute("""
                INSERT INTO positions(userID, symbol, quantity, VWAP)
                VALUES('{}','{}','{}','{}')
                ;""".format(id[0], str(ticker), quantity, float(price)))
        connection.commit()
    else:
        # stock already in position - time to adjust the position
        VWAP_price = VWAP_query[0][0]
        VWAP_quantity = VWAP_query[0][1]
        newVWAPtop = (float(price) * float(quantity)) + (float(VWAP_price) * float(VWAP_quantity))
        newVWAPbottom = (float(VWAP_quantity) + float(quantity))
        VWAP_price = float(newVWAPtop) / float(newVWAPbottom)
        VWAPfinalprice = VWAP_price
        VWAPfinalquantity = newVWAPbottom

        # update quantity
        cursor.execute("""
        UPDATE positions
        SET quantity = '{}'
        WHERE userID = '{}' AND symbol = '{}'
        ;""".format(int(VWAPfinalquantity), id[0], ticker))

        connection.commit()

        # update VWAPprice
        cursor.execute("""
                UPDATE positions
                SET VWAP = '{}'
                WHERE userID = '{}' AND symbol = '{}'
                ;""".format(VWAPfinalprice, id[0], ticker))

        connection.commit()

        VWAP_query = cursor.fetchall()

        connection.commit()

def sell_get_list_of_positions(username):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
                SELECT pk FROM users WHERE name = '{}'
                            ;
                                """.format(username))
    id = cursor.fetchone()

    cursor.execute("""
                SELECT symbol, VWAP, quantity
                FROM positions
                WHERE userID = '{}';
                            """.format(id[0]))
    positions_query = cursor.fetchall()
    if len(positions_query) == 0:
        return False
    else:
        # [ (ticker, price, quantity ) ]
        final_query_list = []
        for tups in positions_query:
            l = []
            for items in tups:
                l.append(items)
            final_query_list.append(l)
        return final_query_list

def sell_stocks_user_table(username, income):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
                SELECT pk FROM users WHERE name = '{}'
                            ;
                                """.format(username))
    id = cursor.fetchone()

    # get current balance
    cursor.execute("""
    SELECT balance FROM users WHERE pk = '{}'
                    ;
                        """.format(id[0]))
    balance = cursor.fetchone()[0]
    new_balance = balance + income

    # update the balance in the USERS table to show that he bought shares
    try:
        cursor.execute("""
                UPDATE users SET balance = '{}' WHERE pk = '{}'
                ;
                    """.format(new_balance, id[0]))
        connection.commit()
        return True, new_balance, income
    except:
        connection.commit()
        return False

def sell_stocks_transactions_table(username, ticker_sell_symbol, ticker_sell_quantity,current_price):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
                    SELECT pk FROM users WHERE name = '{}'
                                ;
                                    """.format(username))
    id = cursor.fetchone()
    now = datetime.datetime.now()

    # update the TRANSACTIONS table to show that we sold shares
    try:
        cursor.execute("""
                    INSERT INTO transactions(userID, symbol, unixtime, lastprice, quantity, buysell)
                    VALUES ('{}','{}','{}','{}','{}','{}')
                    ;
                        """.format(id[0], ticker_sell_symbol, now, current_price, ticker_sell_quantity, 's'))
        connection.commit()
        return True
    except:
        connection.commit()
        return False

def sell_stocks_positions_table(username, ticker_sell_symbol, ticker_sell_quantity,current_price):
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()

    # get primary key from users first
    cursor.execute("""
                SELECT pk FROM users WHERE name = '{}'
                            ;
                                """.format(username))
    id = cursor.fetchone()

    # check if anything in positions exists. If so create VWAP and then UPDATE. Else add to positions.
    cursor.execute("""
                SELECT quantity
                FROM positions
                WHERE userID = '{}' AND symbol = '{}';
                            """.format(id[0], ticker_sell_symbol))
    VWAP_query = cursor.fetchone()
    position_quantity = VWAP_query[0]
    new_position_quantity = position_quantity - ticker_sell_quantity

    # time to subtract the quantity in the position

    cursor.execute("""
        UPDATE positions
        SET quantity = '{}'
        WHERE userID = '{}' AND symbol = '{}'
        ;""".format(new_position_quantity, id[0],ticker_sell_symbol))

    connection.commit()
    return True

def get_all_users():
    connection = sqlite3.connect('db/stocktrade.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
            SELECT name
            FROM users
            ;
                """)
        fetch = cursor.fetchall()
        f2 = []
        for tups in fetch:
            f2.append(list(tups))
        connection.commit()
        return f2
    except:
        connection.commit()
        return False