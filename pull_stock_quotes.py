from urllib2 import Request, urlopen, URLError
import sys
import traceback
from datetime import datetime
import quandl


# Returns pandas DataFrame object containing year-over-year returns between start date and end date, inclusive, for symbols in symbol_list
# Expects str_start_date & str_end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
# Expects all symbols in quandl query format (i.e. All '.' and '-' replaced with '_'
def get_ytd_quandl(symbol_list, str_start_date, str_end_date):
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


# Returns pandas DataFrame object containing closing prices for symbols in symbol_list for the dates between start date and end date, inclusive
# Expects str_start_date & str_end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
# Expects all symbols in quandl query format (i.e. All '.' and '-' replaced with '_'
def get_close_quandl(symbol_list, str_start_date, str_end_date):
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


# Returns list of date & close price for given symbol between start_date and end_date
# Kibot quotes are in format 'Date, Open, Low, High, Close, Volume'
# Note: You must login to Kibot at least once somewhere in your code
# by sending a request to 'http://api.kibot.com/?action=login&user=guest&password=guest'
def get_close_kibot(symbol, str_start_date, str_end_date):
    try:
        url = 'http://api.kibot.com/?action=history&symbol=' + symbol.replace('-','.') +'&interval=daily&startdate=' + datetime.strftime(datetime.strptime(str_start_date, '%Y-%m-%d'), '%x') + '&enddate=' + datetime.strftime(datetime.strptime(str_end_date, '%Y-%m-%d'), '%x')
        response = urlopen(Request(url))
        quotes = response.read().split('\n')[:-1]
        close_prices = list([datetime.strftime(datetime.strptime(quote.split(',')[0],'%m/%d/%Y'),'%Y-%m-%d'), float(quote.split(',')[4])] for quote in quotes)
        return close_prices

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
