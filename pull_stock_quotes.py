from urllib2 import Request, urlopen, URLError
import sys
import traceback
import xml.etree.ElementTree as elTr
import time
from datetime import datetime
import quandl

# Returns pandas DataFrame object containing year-over-year returns between start date and end date
# Expects str_start_date & str_end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
def get_ytd(symbol_list, str_start_date, str_end_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'

        first_day_of_year = '01/01/' + str_start_date[-2:]
        str_start_date = datetime.strftime(datetime.strptime(first_day_of_year, '%x'), '%Y-%m-%d')
        str_end_date = datetime.strftime(datetime.strptime(str_end_date, '%x'), '%Y-%m-%d')

        # Retrieve year-over-year return data for symbol
        quotes = quandl.get(symbol_list, start_date=str_start_date, end_date=str_end_date, collapse="annual", transform="rdiff_from")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + str(symbol_list) + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

def get_alternate_ytd(symbol_info_list, str_start_date, str_end_date):
    dict_ret = {}
    for symbol_inf in symbol_info_list:
        try:
            symbol = symbol_inf.symbol
            symbol = symbol.replace('-','.')
            url = 'http://api.kibot.com/?action=history&symbol=' + symbol +'&interval=daily&startdate=' + str_start_date + '&enddate=' + str_end_date
            request = Request(url)
            response = urlopen(request)
            quotes = response.read().split('\n')
            quotes = quotes[0:len(quotes)-1]
            first_quote = quotes[0]
            last_quote = quotes[len(quotes) - 1]
            first_close = float(first_quote.split(',')[4])
            last_close = float(last_quote.split(',')[4])

            ytd_ret = (last_close - first_close) / first_close
            dict_ret[symbol_inf.symbol] = ytd_ret

        except Exception as e:
            print 'Error retrieving quotes for ' + str(symbol) + ' between ' + str_start_date + ' and ' + str_end_date, e
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    return dict_ret


# Returns pandas DataFrame object containing closing prices for symbols in symbol_list for the dates between start date and end date, inclusive
# Expects str_start_date & str_end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
def get_quotes(symbol_list, str_start_date, str_end_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'

        str_start_date = datetime.strftime(datetime.strptime(str_start_date,'%x'),'%Y-%m-%d')
        str_end_date = datetime.strftime(datetime.strptime(str_end_date,'%x'),'%Y-%m-%d')

        # Retrieve quote data for symbol
        quotes = quandl.get(symbol_list, start_date=str_start_date, end_date=str_end_date, collapse="daily")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + str(symbol_list) + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


# Returns pandas DataFrame object containing a single closing price for the given day
# Expects str_start_date & str_end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
def get_single_quote(symbol, str_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'
        str_date = datetime.strftime(datetime.strptime(str_date,'%x'),'%Y-%m-%d')

        symbol = symbol.replace('-','_').replace('.','_')

        # Retrieve quote data for symbol
        quotes = quandl.get('WIKI/' + symbol + '.11', start_date=str_date, end_date=str_date, collapse="daily")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' on ' + str_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

def get_alternate_quotes(symbol, str_start_date, str_end_date):
    try:
        url = 'http://api.kibot.com/?action=history&symbol=' + symbol +'&interval=daily&startdate=' + str_start_date + '&enddate=' + str_end_date
        request = Request(url)
        response = urlopen(request)
        quotes = response.read().split('\n')
        quotes = quotes[0:len(quotes)-1]
        close_prices = list([datetime.strftime(datetime.strptime(quote.split(',')[0],'%m/%d/%Y'),'%Y-%m-%d'), float(quote.split(',')[4])] for quote in quotes)
        return close_prices

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
