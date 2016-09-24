from urllib2 import Request, urlopen, URLError
import sys
import traceback
import collections
import json

stock_info = collections.namedtuple('stock_info', 'symbol name')

# Takes start_date and end_date in the form mm/dd/YY
def get_symbol_data(symbol):
    try:
        # Retrieve quote data for symbol
        url = 'http://d.yimg.com/aq/autoc?query=' + symbol + '&region=US&lang=en-US'
        request = Request(url)
        response = urlopen(request)
        stock_data = json.loads(response.read())
        result_set = stock_data['ResultSet']
        result = result_set['Result']
        for entry in result:
            if entry['type'] == 'S':
                symbol = entry['symbol']
                name = entry['name']
                break

        ret = stock_info(symbol, name)
        return ret

    except Exception as e:
        print 'Error retrieving stock data for ' + symbol, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

print get_symbol_data('AAPL')
