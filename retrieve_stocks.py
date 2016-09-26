from urllib2 import Request, urlopen, URLError
import finsymbols
import time
import math
from datetime import datetime
import collections
import get_trading_calendar as gtc
import pull_stock_quotes as psq
import pull_stock_data as psd
import build_html
import build_js
import sys, traceback
import SymbolInfo as SI

NUMBER_OF_COMPANIES = 25
symbol_info = collections.namedtuple('symbol_info', 'symbol name query_symbol ytd_return')
dict_returns = {}
dict_quotes = {}
dict_symbol_data = {}
date_list = []
str_start_date = '12/31/15'
str_end_date = time.strftime('%x')
b_alternate_ytd = True

print 'Retrieving valid trading days from  quotes up until ' + str_start_date + ' to ' + str_end_date

# Retrieve list of valid trading days between start and end dates
date_list = gtc.get_trading_days(str_start_date, str_end_date)

print 'Expecting to find quotes for ' + str(len(date_list)) + ' trading days from ' + str_start_date + ' to ' + str_end_date

print 'Retrieving list of S&P500 Constituents'

# Retrieve list of S&P500 constituents
sp500 = finsymbols.get_sp500_symbols()

print 'Retrieved ' + str(len(sp500)) + ' constituents'

# Login to alternate data source in case it is needed
login_url = 'http://api.kibot.com/?action=login&user=guest&password=guest'
request = Request(login_url)
response = urlopen(request)

print 'Retrieving YTD Returns for Constituents'
progress = 0.0
query_symbol_list = []
symbol_info_list = []
# for j in range(90, 93):
#     entry = sp500[j]
for entry in sp500:
    orig_symbol = entry['symbol']
    query_symbol = orig_symbol.replace('-', '_').replace('.', '_')
    symbol_inf = SI.SymbolInfo(orig_symbol, entry['company'], query_symbol, 0)
    query_symbol_list.append('WIKI/' + symbol_inf.query_symbol + '.11')
    symbol_info_list.append(symbol_inf)
    dict_symbol_data[orig_symbol] = symbol_inf

    progress+= 1
    try:

        # Retrieve Returns in batches of 10 for first 500
        if progress % 10 == 0 and progress <= 500:
            if b_alternate_ytd:
                quotes = psq.get_alternate_ytd(symbol_info_list, str_start_date, str_end_date)
            else:
                quotes = psq.get_ytd(query_symbol_list, str_start_date, str_end_date)
            for symbol_inf in symbol_info_list:
                if b_alternate_ytd:
                    ytdRet = quotes[symbol_inf.symbol]
                else:
                    ytdRet = quotes['WIKI/' + symbol_inf.query_symbol + ' - Adj. Close'][0]

                dict_symbol_data[symbol_inf.symbol].ytd_return = round(ytdRet * 100,2)
            query_symbol_list = []
            symbol_info_list = []

        # Get remaining returns
        elif progress == len(sp500):
            if b_alternate_ytd:
                quotes = psq.get_alternate_ytd(symbol_info_list, str_start_date, str_end_date)
            else:
                quotes = psq.get_ytd(query_symbol_list, str_start_date, str_end_date)

            for symbol_inf in symbol_info_list:
                if b_alternate_ytd:
                    ytdRet = quotes[symbol_inf.symbol]
                else:
                    ytdRet = quotes['WIKI/' + symbol_inf.query_symbol + ' - Adj. Close'][0]

                dict_symbol_data[symbol_inf.symbol].ytd_return = round(ytdRet * 100, 2)
            query_symbol_list = []
            symbol_info_list = []
            print 'Retrieved 100% of YTD Returns...'

        if progress % 50 == 0 and progress < 500:
            print 'Retrieved ' + str(round(((progress / 500) * 100), 0)) + '% of YTD Returns...'

    except Exception as e:
        if b_alternate_ytd:
            print 'Error retrieving data for symbol list: ' + str(symbol_info_list), e
        else:
            print 'Error retrieving data for symbol list: ' + str(query_symbol_list), e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        # Get Symbol
    # symbol = entry['symbol']

# Sort map of constituents by return
# Get list of top 25 and bottom 25 performing stocks
try:
    i = 1
    bottom_list = []
    top_list = []

    # Generated sorted map
    sorted_dict = sorted(dict_symbol_data.iteritems(), key=lambda (k, v): (v.ytd_return, k))

    for key, value in sorted_dict:
        if i <= NUMBER_OF_COMPANIES:
            # dict_symbol_data[key].ytd_return = round(value,2)
            bottom_list.append(dict_symbol_data[key])
        else:
            break

        i += 1

    i = 1
    for key, value in reversed(sorted_dict):
        if i <= NUMBER_OF_COMPANIES:
            # dict_symbol_data[key].ytd_return = round(value,2)
            top_list.append(dict_symbol_data[key])
        else:
            break

        i += 1

    print 'Retrieving Full Quote list for Bottom 25 Constituents'
    query_list = []
    for symbol_inf in bottom_list:
        query_list.append('WIKI/' + symbol_inf.query_symbol + '.11')

    # Query Close Data for entire bottom list
    quotes = psq.get_quotes(query_list, str_start_date, str_end_date)
    for symbol_inf in bottom_list:
        b_alternate = False
        close_prices = quotes['WIKI/' + symbol_inf.query_symbol + ' - Adj. Close']
        # if len(close_prices) < len(date_list) or math.isnan(close_prices[0]):
        #     close_prices = psq.get_alternate_quotes(symbol_inf.symbol, str_start_date, str_end_date)
        #     b_alternate = True
        # Calculate daily returns
        j = 0
        prev_close = 0
        daily_returns = []
        for close in close_prices:
            if b_alternate:
                close = close[1]
            if j == 0:
                daily_returns.append(0)
                prev_close = close
            else:
                ret = round((close / prev_close) - 1, 4)
                prev_close = close
                daily_returns.append(ret)
            j+= 1

        # Build two-dimensional matrix of date, closing price, and daily return
        matrix = []
        if b_alternate:
            matrix = [[close_prices[i][0], close_prices[i][1], daily_returns[i]] for i in range(len(close_prices))]
        else:
            matrix = [[list(close_prices.index)[i], close_prices[i], daily_returns[i]] for i in range(len(close_prices))]
        dict_quotes[symbol_inf.symbol] = matrix

    print 'Retrieving Full Quote list for Top 25 Constituents'
    query_list = []
    for symbol_inf in top_list or math.isnan(close_prices[0]):
        query_list.append('WIKI/' + symbol_inf.query_symbol + '.11')

    # Query Close Data for entire bottom list
    quotes = psq.get_quotes(query_list, str_start_date, str_end_date)

    for symbol_inf in top_list:
        close_prices = quotes['WIKI/' + symbol_inf.query_symbol + ' - Adj. Close']
        # if len(close_prices) < len(date_list):
        #     close_prices = psq.get_alternate_quotes(symbol_inf.symbol, str_start_date, str_end_date)

        # Calculate daily returns
        j = 0
        prev_close = 0
        daily_returns = []
        for close in close_prices:
            if b_alternate:
                close = close[1]
            if j == 0:
                daily_returns.append(0)
                prev_close = close
            else:
                ret = round((close / prev_close) - 1, 4)
                prev_close = close
                daily_returns.append(ret)
            j += 1

        # Build two-dimensional matrix of date, closing price, and daily return
        matrix = []
        matrix = [[list(close_prices.index)[i], close_prices[i], daily_returns[i]] for i in range(len(close_prices))]
        dict_quotes[symbol_inf.symbol] = matrix

except Exception as e:
    print 'Error getting top/bottom constituent list', e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

try:
    # Build JavaScript file
    script_list = [build_js.build_javascript_files(top_list, bottom_list, dict_quotes, date_list)]

    # Fuild HTML file
    html_file = build_html.build_html_file(top_list, bottom_list, script_list)

    # Open HTML web page
    build_html.launch_page(html_file)

except Exception as e:
    print 'Error building HTML/JS sites', e
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print "*** print_tb:"
    traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


