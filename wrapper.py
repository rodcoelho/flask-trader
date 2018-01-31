import requests

class Markit:
    def __init__(self):
        self.lookup_url = "http://dev.markitondemand.com/Api/v2/Lookup/json?input="
        self.quote_url = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol="

def get_company_info(string):
    url_concat = "http://dev.markitondemand.com/Api/v2/Lookup/json?input=" + string
    r = requests.get(url_concat)
    data = r.json()
    if r.status_code == 200:
        if len(data) == 0:
            return False, False, False
        else:
            name = data[0]['Name']
            exchange = data[0]['Exchange']
            ticker = data[0]['Symbol']
            # 'Search result: Name {} - Ticker {} - Exchange {}'.format(name, ticker, exchange)
            return name, exchange, ticker
    else:
        return False, False, False


def get_stock_price(string):
    if string is not None:
        url_concat = "http://dev.markitondemand.com/Api/v2/Quote/json?symbol=" + string
        r = requests.get(url_concat)
        if r.status_code == 200:
            data = r.json()
            name = None
            price = None
            if len(data) > 0:
                for key in data:
                    if key == 'LastPrice':
                        price = (data[key])
                    if key == 'Name':
                        name = data[key]
            return [name, price]
        else:
            print('\n\n\n')
            print('API STATUS CODE:' + str(r.status_code))
            print('\n\n\n')
            return [None, None]
    else:
        return [None, None]



if __name__ == "__main__":
    # get company info test
    print(get_company_info('apple'))

    # get stock price test - returns name and price
    print(get_stock_price('aapl'))
