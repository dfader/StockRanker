from urllib2 import Request, urlopen, URLError
from datetime import datetime
import xml.etree.ElementTree as ET
import time

def getMonthCalendar( nYear, nMonth):
    try:
        calUrl = Request('https://api.tradier.com/v1/markets/calendar?year=' + str(nYear) + '&month=' + str(nMonth))
        calResponse = urlopen(calUrl)
        calendar = calResponse.read()
        root = ET.fromstring(calendar)
        return root
    except Exception as e:
        print 'Error retrieving market calendar for ' + str(nMonth) + '/' + str(nYear), e

# Expects an ElementTree root object in the format delivered by https://api.tradier.com/v1/markets/calendar
def countOpenDays(root, bStartMonth, bFinalMonth, dStartDate=datetime.strptime(time.strftime('%x'),'%x'), dEndDate=datetime.strptime(time.strftime('%x'),'%x')):
    count = 0
    days = root[2]
    for day in days.findall('day'):
        if day.find('status').text == 'open':
            if bStartMonth:
                dDate = datetime.strptime(day.find('date').text, '%Y-%m-%d')
                if dDate >= dStartDate:
                    count += 1
            elif bFinalMonth:
                dDate = datetime.strptime(day.find('date').text, '%Y-%m-%d')
                if dDate < dEndDate:
                    count+= 1
            else:
                count+= 1

    return count

# Expects startdate & enddate in the Locale’s appropriate date representation (i.e. %x -> mm/dd/YYYY for US/CA)
# Returns the # of trading days between startdate and enddate
# If current local time > 16:00, return value is inclusive of enddate, else it is exclusive
def getTradingDays( strStartDate, strEndDate):
    nTradingDays = 0
    try:
        print 'Getting # of trading days between ' + strStartDate + ' and ' + strEndDate

        dStartDate = datetime.strptime(strStartDate, '%x')
        dEndDate = datetime.strptime(strEndDate, '%x')

        nStartYear = int(time.strftime('%Y', strStartDate))
        nStartMonth = int(time.strftime('%m', strStartDate))
        nStartDay = int(time.strftime('%d', strStartDate))

        nEndYear = int(time.strftime('%Y', strEndDate))
        nEndMonth = int(time.strftime('%m', strEndDate))
        nEndDay = int(time.strftime('%d', strEndDate))

        if dStartDate > dEndDate:
            raise ValueError('StartDate > EndDate')
        # Get trading days in previous years
        elif nStartYear < nEndYear:
            nFirstMonth = int(time.strftime('%m',strStartDate))

            # Count trading days in first year
            for i in range(nStartMonth, 13):
                root = getMonthCalendar(nStartYear, i)
                if i == nStartMonth:
                    nTradingDays += countOpenDays(root, True, False, dStartDate)
                else:
                    nTradingDays+= countOpenDays(root, False, False)

            nCurYear = nStartYear + 1
            # Count trading days in full year
            while nCurYear < nEndYear:
                for i in range(1,13):
                    root = getMonthCalendar(nCurYear, i)
                    nTradingDays+= countOpenDays(root, False, False)

                nCurYear+= 1

        # Get trading days in final year
        for i in range(1, nEndMonth + 1):
            root = getMonthCalendar(nEndYear, i)
            if i == nEndMonth:
                nTradingDays+= countOpenDays(root, True, dEndDate)
            else:
                nTradingDays+= countOpenDays(root, False, False)

        return nTradingDays
    except Exception as e:
        print 'Error retrieving trading days between ' + strStartDate + ' and ' + strEndDate, e