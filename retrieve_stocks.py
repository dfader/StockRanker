from urllib2 import Request, urlopen
import finsymbols
import time
import collections
import get_trading_calendar as gtc
import pull_stock_quotes as psq
import build_html
import build_js
import sys, traceback
import SymbolInfo as SI

NUMBER_OF_COMPANIES = 25
symbol_info = collections.namedtuple('symbol_info', 'symbol name query_symbol ytd_return')
dict_quotes = {}
dict_symbol_data = {}
date_list = []
str_start_date = '2015-12-31'
str_end_date = time.strftime('%Y-%m-%d')

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
# for j in range(0, 50):
#     entry = sp500[j]
for entry in sp500:

    progress+= 1
    try:
        symbol = entry['symbol']

        # Retrieve Returns in batches of 10 for first 500
        if progress % 50 == 0 and progress <= 500:
            print 'Retrieved ' + str(round(((progress / 500) * 100), 0)) + '% of YTD Returns...'
        elif progress == len(sp500):
            print 'Retrieved 100% of YTD Returns...'

        quotes = psq.get_close_kibot(symbol, str_start_date, str_end_date)
        if quotes[0][0] != date_list[0] or quotes[-1][0] != date_list[-1]:
            print 'Calculating YTD Return between ', quotes[0][0], ' and ', quotes[-1][0], ' for symbol ', symbol
        ytdRet = round(((quotes[-1][1] / quotes[0][1]) - 1) * 100, 2)

        symbol_inf = SI.SymbolInfo(symbol, entry['company'], ytdRet, quotes)
        dict_symbol_data[symbol] = symbol_inf

    except Exception as e:
        print 'Error retrieving data for symbol: ' + str(symbol), e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

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
            bottom_list.append(dict_symbol_data[key])
        else:
            break

        i += 1

    i = 1
    for key, value in reversed(sorted_dict):
        if i <= NUMBER_OF_COMPANIES:
            top_list.append(dict_symbol_data[key])
        else:
            break

        i += 1

    print 'Calculating daily returns for Bottom 25 Constituents'
    for symbol_inf in bottom_list:
        quotes = symbol_inf.quotes

        # Calculate daily returns
        j = 0
        prev_close = 0
        daily_returns = []
        for quote in quotes:
            close = quote[1]
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
        matrix = [[quotes[i][0], quotes[i][1], daily_returns[i]] for i in range(len(quotes))]
        dict_quotes[symbol_inf.symbol] = matrix

    print 'Calculating daily returns for Top 25 Constituents'
    query_list = []
    for symbol_inf in top_list:
        quotes = symbol_inf.quotes

        # Calculate daily returns
        j = 0
        prev_close = 0
        daily_returns = []
        for quote in quotes:
            close = quote[1]
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
        matrix = [[quotes[i][0], quotes[i][1], daily_returns[i]] for i in range(len(quotes))]
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


