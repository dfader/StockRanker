import build_js
import build_html
import collections


ytd_return = collections.namedtuple('ytd_return', 'symbol ytd_return')
stock_data = collections.namedtuple('stock_data', 'symbol name ')

top_stock_1_ret = ytd_return('AAPL', 23.34)
top_stock_2_ret = ytd_return('NFLX', 12.34)

bottom_stock_1_ret = ytd_return('IBM', -43.34)
bottom_stock_2_ret = ytd_return('CCJ', -12.34)

top_stock_1_data = stock_data('AAPL', 'Apple Inc.')
top_stock_2_data = stock_data('NFLX', 'Netflix Inc.')

bottom_stock_1_data = stock_data('IBM', 'International Business Machines')
bottom_stock_2_data = stock_data('CCJ', 'Cameco Corp.')

bottom_list = [bottom_stock_1_ret, bottom_stock_2_ret]
top_list = [top_stock_1_ret, top_stock_2_ret]
dict_data = {}
dict_data[top_stock_1_data.symbol] = top_stock_1_data
dict_data[top_stock_2_data.symbol] = top_stock_2_data
dict_data[bottom_stock_1_data.symbol] = bottom_stock_1_data
dict_data[bottom_stock_2_data.symbol] = bottom_stock_2_data

script_list = [build_js.build_javascript_files(top_list, bottom_list)]
html_file = build_html.build_html_file(top_list, bottom_list, dict_data, script_list)
build_html.launch_page(html_file)