from urllib2 import Request, urlopen, URLError
import finsymbols
import time
from datetime import datetime
import collections
import xml.etree.ElementTree as ET

ytdReturn = collections.namedtuple('ytdReturn', 'symbol ytdReturn')
dict_returns = {}
dict_quotes = {}
symbols = []
nTradingDays = 0

try:

    today = time.strftime("%x")
    print 'Retrieving stock quotes up until ' + today

    nMonth = int(time.strftime("%m"))
    strYear = time.strftime("%Y")
    for i in range(1, nMonth + 1):
        calUrl = Request('https://api.tradier.com/v1/markets/calendar?year=' + strYear + '&month=' + str(i))
        calResponse = urlopen(calUrl)
        calendar = calResponse.read()
        root = ET.fromstring(calendar)
        days = root[2]
        for day in days.findall('day'):
            if day.find('status').text == 'open':
                if i == nMonth:
                    dDate = datetime.strptime(day.find('date').text,'%Y-%m-%d')
                    dTodaysDate = datetime.strptime(today,'%x')
                    if dDate < dTodaysDate:
                        nTradingDays += 1
                else:
                    nTradingDays+= 1


    print 'Expecting to find quotes for ' + str(nTradingDays) + ' trading days so far in calendar year ' + strYear
except Exception as e:
    print 'Error retrieving market calendar', e

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
    exit(0)

print 'Retrieving Quotes for Constituents'
for entry in sp500:
    try:
        # Get Symbol
        symbol = entry['symbol']
        symbol = symbol.replace('-','.')
        symbols.append(symbol)

        # Retrieve quote data for symbol
        url = 'http://api.kibot.com/?action=history&symbol=' + symbol + '&interval=daily&startdate=01/01/2016&enddate='+today
        request = Request(url)
        response = urlopen(request)
        quoteData = response.read()
        quotes = quoteData.split("\n")
        quotes.pop(len(quotes)-1)

        if len(quotes) != nTradingDays:
            print 'Missing data for ' + symbol + '. Expected ' + str(nTradingDays) + ' trading days but got ' + str(len(quotes))
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

try:
    i = 1
    bottomList = []
    topList = []
    for key, value in sorted(dict_returns.iteritems(), key=lambda (k, v): (v, k)):
        if i <= 25:
            bottomList.append(ytdReturn(key, value))
        else:
            break

        i += 1

    i = 1
    for key, value in sorted(dict_returns.iteritems(), key=lambda (k, v): (v, k),reverse=True):
        if i <= 25:
            topList.append(ytdReturn(key, value))
        else:
            break

        i+=1

    for pair in bottomList:
        print pair.symbol, str(pair.ytdReturn)

    for pair in topList:
        print pair.symbol, str(pair.ytdReturn)

except Exception as e:
    print 'Error getting top/bottom list', e


