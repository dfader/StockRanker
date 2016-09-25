from urllib2 import Request, urlopen
from datetime import datetime
import xml.etree.ElementTree as elTr
import time
import sys
import traceback

def get_month_calendar(n_year, n_month):
    try:
        cal_url = Request('https://api.tradier.com/v1/markets/calendar?year=' + str(n_year) + '&month=' + str(n_month))
        cal_response = urlopen(cal_url)
        calendar = cal_response.read()
        root = elTr.fromstring(calendar)
        return root
    except Exception as e:
        print 'Error retrieving market calendar for ' + str(n_month) + '/' + str(n_year), e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


# Expects an ElementTree root object in the format delivered by https://api.tradier.com/v1/markets/calendar
def get_open_days(root, b_start_month, b_final_month,
                  d_start_date=datetime.strptime(time.strftime('%x'), '%x'),
                  d_end_date=datetime.strptime(time.strftime('%x'), '%x')):
    date_list = []
    str_year = root[0].text
    str_month = root[1].text
    days = root[2]
    for day in days.findall('day'):
        if day.find('status').text == 'open':
            if b_start_month:
                d_date = datetime.strptime(day.find('date').text, '%Y-%m-%d')
                if d_date >= d_start_date:
                    date_list.append(day.find('date').text)
            elif b_final_month:
                d_date = datetime.strptime(day.find('date').text, '%Y-%m-%d')
                if d_date < d_end_date:
                    date_list.append(day.find('date').text)
                elif d_date == d_end_date:
                    cur_hour = time.strftime('%H')
                    cur_min = time.strftime('%M')
                    if cur_hour >= 16 and cur_min >= 10:
                        date_list.append(day.find('date').text)
            else:
                date_list.append(day.find('date').text)

    return date_list


# Expects start_date & end_date in the Locale's appropriate date representation (i.e. %x -> mm/dd/YY for US/CA)
# Returns the # of trading days between start_date and end_date
# If current local time > 16:00, return value is inclusive of end_date, else it is exclusive
def get_trading_days(str_start_date, str_end_date):
    date_list = []
    try:
        print 'Getting # of trading days between ' + str_start_date + ' and ' + str_end_date

        d_start_date = datetime.strptime(str_start_date, '%x')
        d_end_date = datetime.strptime(str_end_date, '%x')

        n_start_year = d_start_date.year
        n_start_month = d_start_date.month

        n_end_year = d_end_date.year
        n_end_month = d_end_date.month

        if d_start_date > d_end_date:
            raise ValueError('StartDate > End_date')
        # Get trading days in previous years
        elif n_start_year < n_end_year:

            # Count trading days in first year
            for i in range(n_start_month, 13):
                root = get_month_calendar(n_start_year, i)
                if i == n_start_month:
                    date_list += get_open_days(root, True, False, d_start_date)
                else:
                    date_list += get_open_days(root, False, False)

            n_cur_year = n_start_year + 1
            # Count trading days in full year
            while n_cur_year < n_end_year:
                for i in range(1, 13):
                    root = get_month_calendar(n_cur_year, i)
                    date_list += get_open_days(root, False, False)

                n_cur_year += 1

        # Get trading days in final year
        for i in range(1, n_end_month + 1):
            root = get_month_calendar(n_end_year, i)
            if i == n_end_month:
                date_list += get_open_days(root, False, True, d_end_date)
            else:
                date_list += get_open_days(root, False, False)

        return date_list
    except Exception as e:
        print 'Error retrieving trading days between ' + str_start_date + ' and ' + str_end_date, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)