## Flask Trader

Terminal Trader on Flask microframework. 

This assumes you have the latest version of Python3 and Flask.

#### Step 1: Clone the repository

Run `$ git clone https://github.com/rodcoelho/flask-trader.git` in your terminal.

#### Step 2: Set up database

1) `$ chmod +x ./setup.sh` 
2) `$ chmod +x ./run.sh`
3) `$ ./setup.sh`

This creates the sqlite3 database in `db/stocktrade.db` 
and allows the application to store stock data and track the user

#### Step 3: Launch the website

Run `$ ./run.sh` on your terminal

On your browser visit: `http://127.0.0.1:5000/`

User will start with $1,000,000 in cash and own no assets.
 
Look up stock symbols, price, buy and sell assets. 

#### Step 4: Close the application

In your terminal, press Control+C to terminate the app.
