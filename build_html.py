import webbrowser
import sys
import traceback


def build_html_file(top_list, bottom_list, dict_data, script_list):
    try:
        f = open('StockRanker.html', 'w')

        top_stocks_table = build_table(top_list, dict_data, 'top_list_table_id')
        bottom_stocks_table = build_table(bottom_list, dict_data, 'bottom_list_table_id')
        message = """<html><head>
                    <link rel="stylesheet" type="text/css" href="DataTables/css/jquery.dataTables.min.css">
                    <link rel="stylesheet" type="text/css" href="Select-1.2.0/css/select.dataTables.min.css">
                    <link rel="stylesheet" type="text/css" href="css/StockRanker.css">
                    <script type="text/javascript" charset="utf8" src="js/jquery-1.12.3.js"></script>
                    <script type="text/javascript" charset="utf8" src="js/loader.js"></script>
                    <script type="text/javascript" charset="utf8" src="js/datatables.min.js"></script>
                    <script type="text/javascript" charset="utf8" src="Select-1.2.0/js/dataTables.select.min.js"></script>"""


        for script in script_list:
            message += """<script type="text/javascript" charset="utf8" src=\"""" + script + """"></script>"""

        message+="""</head>
                    <body><br>
                        <div class="page_header">S&P 500 YTD Performance 2016</div>
                        <br><br>
                        <div class="tables_div">
                            <div class="ranking_div">
                                <div class=table_title>25 Best Performing Stocks YTD</div>
                                <br>
                                <div class=ranking_table>""" + top_stocks_table + """</div>
                            </div>
                            <div class="ranking_div">
                                <div class=table_title>25 Worst Performing Stocks YTD</div>
                                <br>
                                <div class=ranking_table>""" + bottom_stocks_table + """</div>
                            </div>
                        </div>
                        <br>
                        <div id="chart_title"></div>
                        <div id="dashboard">
                            <div id="chart_div"></div>
                            <div id="control_div"></div>
                        </div>
                    <br></body></html>"""

        f.write(message)
        f.close()
        return f.name

    except Exception as e:
        print 'Error building HTML file', e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


def launch_page(file_name):
    try:
        webbrowser.open_new_tab(file_name)
    except Exception as e:
        print 'Error launching HTML file', e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


def build_table(stock_list, dict_data, table_id):
    try:
            html_table = """<table id=\"""" + table_id + """" class="stock_table">
                        <thead>
                        <tr class="table_header">
                            <th>Stock Symbol</th>
                            <th>Name</th>
                            <th>YTD Return %</th>
                        </tr>
                        </thead><tbody>"""

            for stock in stock_list:
                stock_data = dict_data[stock.symbol]
                html_table += """<tr id=\"""" + stock.symbol + """">
                              <td class="center_col">""" + stock.symbol + """</td>
                              <td>""" + stock_data.name + """</td>
                              <td class="center_col">""" + str(stock.ytd_return) + """</td>
                              </tr>"""

            html_table += "</tbody></table>"
            return html_table
    except Exception as e:
        print 'Error building table ' + table_id, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
