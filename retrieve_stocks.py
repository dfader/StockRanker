from urllib2 import Request, urlopen, URLError
import finsymbols
import time
from datetime import datetime
import collections
import get_trading_calendar as gtc
import pull_stock_quotes as psq
import pull_stock_data as psd
import build_html
import build_js
import sys, traceback

ytd_return = collections.namedtuple('ytd_return', 'symbol ytd_return')
date_quote = collections.namedtuple('date_quote', 'date price')
dict_returns = {}
dict_quotes = {}
dict_data = {}
date_list = []
str_start_date = '12/31/15'
str_end_date = time.strftime('%x')

def get_quotes(symbol):
    return dict_quotes[symbol]

try:
    today = time.strftime("%x")
    print 'Retrieving stock quotes up until ' + today

    n_year = datetime.strptime(str_end_date, '%x').year
    date_list = gtc.get_trading_days(str_start_date, str_end_date)
    print 'Expecting to find quotes for ' + str(len(date_list)) + ' trading days so far in calendar year ' + str(n_year)

except Exception as e:
    print 'Error retrieving market calendar', e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

try:
    # Login to api site
    login = Request('http://api.kibot.com/?action=login&user=guest&password=guest')
    urlopen(login)

    # Retrieve list of S&P500 constituents
    print 'Retrieving list of S&P500 Constituents'
    sp500 = finsymbols.get_sp500_symbols()
    print 'Retrieved ' + str(len(sp500)) + ' constituents'

except Exception as e:
    print 'Error retrieving list of S&P500 companies'
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    exit(0)

print 'Retrieving Quotes for Constituents'
progress = 0.0
# for j in range(0, 6):
#     entry = sp500[j]
for entry in sp500:
    progress+= 1
    if progress % 50 == 0:
        print 'Retrieved ' + str(round(((progress / 500) * 100), 0)) + '% of quotes...'

    try:
        # Get Symbol
        symbol = entry['symbol']

        # quotes = psq.get_quotes(symbol, str_start_date, str_end_date)
        # quotes += psq.get_single_quote(symbol, '09/23/16')
        # if len(quotes) != len(date_list):
        #     print 'Missing data for ' + symbol + \
        #           '. Expected ' + str(len(date_list)) + \
        #           ' trading days but got ' + str(len(quotes))
        #     # print quotes
        # else:
        # lastClose = quotes['Adj. Close'][len(quotes) - 1]
        # firstOpen = quotes['Adj. Open'][0]
        # lastQuote = quotes[len(quotes) - 1]
        # firstQuote = quotes[0]
        # lastClose = float(lastQuote.find('Close').text)
        # firstOpen = float(firstQuote.find('Open').text)
        # lastVals = lastQuote.split(',')
        # firstVals = firstQuote.split(',')
        # if len(lastVals) != 6:
        #     print 'Error in quote formatting of final quote for symbol ' + symbol + ':' + lastQuote
        # elif len(firstVals) != 6:
        #     print 'Error in quote formatting of first quote for symbol ' + symbol + ':' + firstQuote
        # else:
        #     lastClose = float(lastVals[4])
        #     firstOpen = float(firstVals[1])
        # ytdRet = (lastClose - firstOpen) / firstOpen

        quotes = psq.get_YTD(symbol, str_start_date, str_end_date)
        ytdRet = quotes['Adj. Close'][0]
        dict_returns[symbol] = ytdRet * 100
    except Exception as e:
        print 'Error retrieving data from entry ' + str(entry), e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

try:
    i = 1
    bottom_list = []
    top_list = []
    for key, value in sorted(dict_returns.iteritems(), key=lambda (k, v): (v, k)):
        if i <= 25:
            bottom_list.append(ytd_return(key, round(value,2)))
        else:
            break

        i += 1

    i = 1
    for key, value in sorted(dict_returns.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        if i <= 25:
            top_list.append(ytd_return(key, round(value,2)))
        else:
            break

        i += 1

    for pair in bottom_list:
        stock_info = psd.get_symbol_data(pair.symbol)
        dict_data[pair.symbol] = stock_info
        quotes = psq.get_quotes(pair.symbol, str_start_date, str_end_date)
        close_prices = quotes['Adj. Close']
        matrix = []
        for i in range(len(close_prices)):
            matrix.append([list(close_prices.index)[i], close_prices[i]])
        dict_quotes[pair.symbol] = matrix
#        print pair.symbol, str(pair.ytd_return)

    for pair in top_list:
        stock_info = psd.get_symbol_data(pair.symbol)
        dict_data[pair.symbol] = stock_info
        quotes = psq.get_quotes(pair.symbol, str_start_date, str_end_date)
        close_prices = quotes['Adj. Close']
        matrix = [[list(close_prices.index)[i], close_prices[i]] for i in range(len(close_prices))]
        dict_quotes[pair.symbol] = matrix
#        print pair.symbol, str(pair.ytd_return)

    script_list = [build_js.build_javascript_files(top_list, bottom_list, dict_quotes, date_list)]
    html_file = build_html.build_html_file(top_list, bottom_list, dict_data, script_list)
    build_html.launch_page(html_file)

except Exception as e:
    print 'Error getting top/bottom list', e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

