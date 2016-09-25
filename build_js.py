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
                # vals = quote.split(',')
                # close = vals[4]
                date = str(quote[0])[:10]
                close = quote[1]
                message += """['""" + date + """','""" + str(close) + """'],"""

            # Remove final trailing comma
            message = message[:len(message) - 1]
            message+= """],
                        """

        # Define map of all symbols/quotes for bottom_list
        for pair in bottom_list:
            symbol = pair.symbol
            message+= """'""" + symbol + """': ["""
            for quote in quotes[symbol]:
                # vals = quote.split(',')
                # close = vals[4]
                date = str(quote[0])[:10]
                close = quote[1]
                message += """['""" + date + """','""" + str(close) + """'],"""

            # Remove final trailing comma
            message = message[:len(message) - 1]
            message+= """],"""

        # Remove trailing whitespace and comma
        message = message[:len(message) - 1]
        message+="""};
                var date_list=""" + str(date_list) + """;
                var chart_array=[[],[]];
                var range_start;
                var range_end;
                var symbol;

                google.charts.load('visualization', '1', {packages: ['controls', 'charteditor', 'corechart']});
                google.charts.setOnLoadCallback(drawChart);

                function drawPriceChart(symbol, range_start, range_end){
                    chart_title = document.getElementById('chart_title');
                    chart_title.innerHTML = symbol + ' Price Chart';
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
                                'start': new Date(range_start),
                                'end': new Date(range_end)
                            }
                        }
                    });

                    var chart = new google.visualization.ChartWrapper({
                        chartType: 'LineChart',
                        containerId: 'chart_div',
                        'options':{
                            width: '100%',
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
                        this.range_start = v.range.start;
                        this.range_end = v.range.end;
                        return 0;
                    });
                }

                function drawChart(){
                    if (this.symbol == null)
                        this.symbol = Object.keys(dict_quotes)[0];
                    symbol = this.symbol;

                    loadChart(symbol);
                }

                $(document).ready( function () {
                        var top_table = $('#top_list_table_id').DataTable({
                            select: {
                                style: "single"
                            },
                            scrollY: '50vh',
                            scrollCollapse: true,
                            "order": [[ 2, "desc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ],
                            responsive: true,
                            columnDefs: [
                                { responsivePriority: 1, targets: 0 },
                                { responsivePriority: 2, targets: -1 }
                            ]
                        });
                        var bottom_table = $('#bottom_list_table_id').DataTable({
                            select: {
                                style: "single"
                            },
                            scrollY: '50vh',
                            scrollCollapse: true,
                            "order": [[ 2, "asc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ],
                            responsive: true,
                            columnDefs: [
                                { responsivePriority: 1, targets: 0 },
                                { responsivePriority: 2, targets: -1 }
                            ]
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

                    //create trigger to resizeEnd event
                    $(window).resize(function() {
                        if(this.resizeTO) clearTimeout(this.resizeTO);
                        this.resizeTO = setTimeout(function() {
                            $(this).trigger('resizeEnd');
                        }, 500);
                    });

                    //redraw graph when window resize is completed
                    $(window).on('resizeEnd', function() {
                        drawChart();
                    });

                    function loadChart(symbol){
                        this.symbol = symbol;
                        quotes = dict_quotes[symbol];
                        var length = date_list.length;
                        var prevQuote = 0.0;
                        var j = 0;
                        for(i=0; i<length; i++){
				            var next_expected_date = new Date(date_list[i]);
				            var next_quote_date = new Date(quotes[j][0]);
				            var quote = prevQuote;
				            if (next_expected_date.getTime() == next_quote_date.getTime()){
				                quote = parseFloat(quotes[j][1]);
				                prevQuote = quote;
				                j++;
				            }
                            var item = [];
                            item[0] = next_expected_date;
                            item[1] = quote;
                            chart_array[i] = item;
                        }

                        var start_date = new Date('2016-01-01');
                        var end_date = new Date('2016-09-23');
                        if (this.range_start != null){
                            start_date = this.range_start;
                        }

                        if (this.range_end != null){
                            end_date = this.range_end;
                        }

                        drawPriceChart(symbol, start_date, end_date);
                    }
                    """

        f.write(message)
        f.close()
        return f.name

    except Exception as e:
        print 'Error building JavaScript file', e
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "*** print_tb:"
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
