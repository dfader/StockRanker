from urllib2 import Request, urlopen, URLError
import sys
import traceback
import xml.etree.ElementTree as elTr
import time
from datetime import datetime
import quandl

def get_YTD(symbol, str_start_date, str_end_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'

        str_start_date = datetime.strftime(datetime.strptime(str_start_date, '%x'), '%Y-%m-%d')
        str_end_date = datetime.strftime(datetime.strptime(str_end_date, '%x'), '%Y-%m-%d')

        symbol = symbol.replace('-','_').replace('.','_')

        quotes = quandl.get('WIKI/' + symbol, start_date=str_start_date, end_date=str_end_date, collapse="annual", transform="rdiff_from")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


# Takes start_date and end_date in the form mm/dd/YY
def get_quotes(symbol, str_start_date, str_end_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'

        str_start_date = datetime.strftime(datetime.strptime(str_start_date,'%x'),'%Y-%m-%d')
        str_end_date = datetime.strftime(datetime.strptime(str_end_date,'%x'),'%Y-%m-%d')

        symbol = symbol.replace('-','_').replace('.','_')

        # Retrieve quote data for symbol
        # url = 'http://api.kibot.com/?action=history&symbol=' + symbol + '&interval=daily&startdate=' + str_start_date + '&enddate=' + str_end_date
        # url = """https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.historicaldata%20where%20symbol%20%3D%20%22""" + symbol + """%22%20and%20startDate%20%3D%20%22""" + str_start_date + """%22%20and%20endDate%20%3D%20%22""" + str_end_date + """%22&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"""
        # request = Request(url)
        # response = urlopen(request)
        # quote_data = response.read()

        # root = elTr.fromstring(quote_data)
        # quotes = root[1].findall('quote')
        quotes = quandl.get('WIKI/' + symbol, start_date=str_start_date, end_date=str_end_date, collapse="daily")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

def get_single_quote(symbol, str_date):
    try:
        quandl.ApiConfig.api_key = 'oDRExdcWoyruPUL3p34T'
        str_date = datetime.strftime(datetime.strptime(str_date,'%x'),'%Y-%m-%d')

        symbol = symbol.replace('-','_').replace('.','_')

        # Retrieve quote data for symbol
        # url = 'http://api.kibot.com/?action=history&symbol=' + symbol + '&interval=daily&startdate=' + str_date + '&enddate=' + str_date
        # request = Request(url)
        # response = urlopen(request)
        # quote_data = response.read()

        # root = elTr.fromstring(quote_data)
        # quotes = root[1].findall('quote')

        # quotes = quote_data.split("\n")
        # quotes.pop(len(quotes) - 1)
        quotes = quandl.get('WIKI/' + symbol, start_date=str_date, end_date=str_date, collapse="daily")

        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' on ' + str_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)