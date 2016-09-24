from urllib2 import Request, urlopen, URLError
import sys
import traceback

# Takes start_date and end_date in the form mm/dd/YY
def get_quotes(symbol, str_start_date, str_end_date):
    try:
        # Retrieve quote data for symbol
        url = 'http://api.kibot.com/?action=history&symbol=' + symbol + '&interval=daily&startdate=' + str_start_date + '&enddate=' + str_end_date
        request = Request(url)
        response = urlopen(request)
        quote_data = response.read()

        quotes = quote_data.split("\n")
        quotes.pop(len(quotes) - 1)
        return quotes

    except Exception as e:
        print 'Error retrieving quotes for ' + symbol + ' between ' + str_start_date + ' and ' + str_end_date
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)