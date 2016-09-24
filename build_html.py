import webbrowser
import sys
import traceback


def build_html_file(top_list, bottom_list, dict_data, script_list):
    try:
        f = open('StockRanker.html', 'w')

        top_stocks_table = build_table(top_list, dict_data, 'top_list_table_id')
        print top_stocks_table
        bottom_stocks_table = build_table(bottom_list, dict_data, 'bottom_list_table_id')
        print bottom_stocks_table
        message = """<html><head>
                    <link rel="stylesheet" type="text/css" href="DataTables/css/jquery.dataTables.min.css">
                    <link rel="stylesheet" type="text/css" href="css/StockRanker.css">
                    <script type="text/javascript" charset="utf8" src="js/jquery-1.12.3.js"></script>
                    <script type="text/javascript" charset="utf8" src="DataTables/js/jquery.dataTables.min.js"></script>"""


        for script in script_list:
            message += """<script type="text/javascript" charset="utf8" src=\"""" + script + """"></script>"""

        message+="""</head>
                    <body><br>
                        <div class="tables_div">
                            <div class="ranking_table">""" + top_stocks_table + """</div>
                            <div class="ranking_table">""" + bottom_stocks_table + """</div>
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
            html_table = """<table id=\"""" + table_id + """"><thead>
                         <th>Stock Symbol</th>
                         <th>Name</th>
                         <th>YTD Return %</th>
                         </thead><tbody>"""

            for stock in stock_list:
                stock_data = dict_data[stock.symbol]
                html_table += """<tr>
                              <td>""" + stock.symbol + """</td>
                              <td>""" + stock_data.name + """</td>
                              <td>""" + str(stock.ytd_return) + """</td>
                              </tr>"""

            html_table += "</tbody></table>"
            return html_table
    except Exception as e:
        print 'Error building table ' + table_id, e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
