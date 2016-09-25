import sys
import traceback


def build_javascript_files(top_list, bottom_list, quotes, date_list):
    try:
        f = open('js/StockRanker.js', 'w')

        # Define map of all symbols/quotes for top_list
        message = """var dict_quotes={"""
        for pair in top_list:
            symbol = pair.symbol
            message+= """'""" + symbol + """': ["""
            for quote in quotes[symbol]:
                vals = quote.split(',')
                close = vals[4]
                message += """'""" + close + """',"""

            # Remove final trailing comma
            message = message[:len(message) - 1]
            message+= """],
                        """

        # Define map of all symbols/quotes for bottom_list
        for pair in bottom_list:
            symbol = pair.symbol
            message+= """'""" + symbol + """': ["""
            for quote in quotes[symbol]:
                vals = quote.split(',')
                close = vals[4]
                message += """'""" + close + """',"""

            # Remove final trailing comma
            message = message[:len(message) - 1]
            message+= """],"""

        # Remove trailing whitespace and comma
        message = message[:len(message) - 1]
        message+="""};
                var date_list=""" + str(date_list) + """;
                var chart_array=[[],[]];

                function drawPriceChart(rangeStart, rangeEnd){
                    var data = new google.visualization.DataTable();
                    data.addColumn('date', 'Date');
                    data.addColumn('number', 'Close Price');
                    for (var i = 0; i < date_list.length; i++) {
                        data.addRow([chart_array[i][0], chart_array[i][1]]);
                    }

                    var dash = new google.visualization.Dashboard(document.getElementById('dashboard'));
                    var control = new google.visualization.ControlWrapper({
                        'controlType': 'ChartRangeFilter',
                        'containerId': 'control_div',
                        'options': {
                            'backgroundColor': '#14894e',
                            'filterColumnIndex': 0,
                            'ui': {
                                'chartOptions': {
                                    height: 30,
                                    width: '100%',
                                    chartArea: {
                                        width: '80%'
                                    },
                                    hAxis: {
                                      'textPosition': 'in',
                                      'titleTextStyle': {color: '#000000'},
                                      'textStyle':{color: '#000000'},
                                    },
                                    vAxis: {
                                      'textPosition': 'none',
                                      'titleTextStyle': {color: '#000000'},
                                      'textStyle':{color: '#000000'},
                                      'gridlines': {'color': 'none'}
                                    },
                                 'backgroundColor': { fill:'transparent' },
                                }
                                ,
                                snapToData: true,
                            }
                        },
                        'state':{
                            'range': {
                                'start': new Date(rangeStart),
                                'end': new Date(rangeEnd)
                            }
                        }
                    });

                    var chart = new google.visualization.ChartWrapper({
                        chartType: 'LineChart',
                        containerId: 'chart_div',
                        'options':{
                            'backgroundColor': { fill:'transparent' },
                            'legend': {position: 'top', alignment: 'start'},
                            'lineWidth': 4,
                            'series': {
                                0: { lineDashStyle: [0, 0] }
                            },
                            'colors': ['#e2431e'],
                            'hAxis': {
                              title: 'Date',
                              titleTextStyle: {color: '#000000'},
                              textStyle:{color: '#000000'},
                              bold: true
                            },
                            'vAxis': {
                              title: 'Price',
                              titleTextStyle: {color: '#000000'},
                              textStyle:{color: '#000000'},
                              bold: true
                            },
                            legend: {
                                textStyle: {color: '#000000'},
                                position: 'right'
                            }
                        }
                    });

                    function setOptions (wrapper) {
                        wrapper.setOption('width', '100%');
                        wrapper.setOption('chartArea.width', '80%');
                    }

                    setOptions(chart);

                    dash.bind([control], [chart]);
                    dash.draw(data);
                    google.visualization.events.addListener(control, 'statechange', function () {
                        var v = control.getState();
                        this.rangeStart = v.range.start;
                        return 0;
                    });
                }

                function drawChart(){
                    var startDate = new Date('2016-01-01');
                    var endDate = new Date('2016-09-23');
                    drawPriceChart(startDate, endDate);
                }

                $(document).ready( function () {
                        var top_table = $('#top_list_table_id').DataTable({
                            select: {
                                style: "single"
                            },
                            "order": [[ 2, "desc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ]
                        });
                        var bottom_table = $('#bottom_list_table_id').DataTable({
                            select: {
                                style: "single"
                            },
                            "order": [[ 2, "asc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ]
                        });

                        top_table.on( 'select', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = top_table.rows( indexes ).data().pluck( 0 );

                                loadChart(data[0]);
                            }
                        } );

                        bottom_table.on( 'select', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = bottom_table.rows( indexes ).data().pluck( 0 );

                                loadChart(data[0]);
                            }
                        } );
                    } );

                    function loadChart(symbol){
                        quotes = dict_quotes[symbol];
                        var length = quotes.length;
                        for(i=0; i<length; i++){
				            var next_date = new Date(date_list[i]);
				            var quote = parseFloat(quotes[i]);
                            var item = [];
                            item[0] = next_date;
                            item[1] = quote;
                            chart_array[i] = item;
                        }

                        google.charts.load('visualization', '1', {packages: ['controls', 'charteditor', 'corechart']});
                        google.charts.setOnLoadCallback(drawChart);

                        console.log(chart_array);
                    }
                    """

        f.write(message)
        f.close()
        return f.name

    except Exception as e:
        print 'Error building HTML file', e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
