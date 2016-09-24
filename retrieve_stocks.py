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
dict_returns = {}
dict_quotes = {}
dict_data = {}
symbols = []
n_trading_days = 0
str_start_date = '01/01/16'
str_end_date = time.strftime('%x')

try:
    today = time.strftime("%x")
    print 'Retrieving stock quotes up until ' + today

    n_year = datetime.strptime(str_end_date, '%x').year
    n_trading_days = gtc.get_trading_days(str_start_date, str_end_date)
    print 'Expecting to find quotes for ' + str(n_trading_days) + ' trading days so far in calendar year ' + str(n_year)

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
for j in range(1, 10):
    entry = sp500[j]
#for entry in sp500:
    progress+= 1
    if progress % 50 == 0:
        print 'Retrieved ' + str(round(((progress / 500) * 100), 0)) + '% of quotes...'

    try:
        # Get Symbol
        symbol = entry['symbol']
        symbol = symbol.replace('-', '.')
        symbols.append(symbol)

        quotes = psq.get_quotes(symbol, str_start_date, str_end_date)
        if len(quotes) != n_trading_days:
            print 'Missing data for ' + symbol + \
                  '. Expected ' + str(n_trading_days) + \
                  ' trading days but got ' + str(len(quotes))
            # print quoteData
        else:
            lastQuote = quotes[len(quotes) - 1]
            firstQuote = quotes[0]
            lastVals = lastQuote.split(',')
            firstVals = firstQuote.split(',')
            if len(lastVals) != 6:
                print 'Error in quote formatting of final quote for symbol ' + symbol + ':' + lastQuote
            elif len(firstVals) != 6:
                print 'Error in quote formatting of first quote for symbol ' + symbol + ':' + firstQuote
            else:
                lastClose = float(lastVals[4])
                firstOpen = float(firstVals[1])
                ytdRet = (lastClose - firstOpen) / firstOpen
                dict_returns[symbol] = ytdRet * 100
                dict_quotes[symbol] = quotes
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
            bottom_list.append(ytd_return(key, value))
        else:
            break

        i += 1

    i = 1
    for key, value in sorted(dict_returns.iteritems(), key=lambda (k, v): (v, k), reverse=True):
        if i <= 25:
            top_list.append(ytd_return(key, value))
        else:
            break

        i += 1

    for pair in bottom_list:
        stock_info = psd.get_symbol_data(pair.symbol)
        dict_data[pair.symbol] = stock_info
#        print pair.symbol, str(pair.ytd_return)

    for pair in top_list:
        stock_info = psd.get_symbol_data(pair.symbol)
        dict_data[pair.symbol] = stock_info
#        print pair.symbol, str(pair.ytd_return)

    print 'dict_data: ', dict_data
    script_list = []
    script_list.append(build_js.build_javascript_files(top_list, bottom_list))
    html_file = build_html.build_html_file(top_list, bottom_list, dict_data, script_list)
    build_html.launch_page(html_file)

except Exception as e:
    print 'Error getting top/bottom list', e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

