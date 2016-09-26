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
                date = str(quote[0])[:10]
                close = quote[1]
                ret = quote[2]
                message += """['""" + date + """','""" + str(close) + """','""" + str(ret) + """'],"""

            # Remove final trailing comma
            message = message[:len(message) - 1]
            message+= """],
                        """

        # Define map of all symbols/quotes for bottom_list
        for pair in bottom_list:
            symbol = pair.symbol
            message+= """'""" + symbol + """': ["""
            for quote in quotes[symbol]:
                date = str(quote[0])[:10]
                close = quote[1]
                ret = quote[2]
                message += """['""" + date + """','""" + str(close) + """','""" + str(ret) + """'],"""

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
                var symbol_list = [];

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
                                      'titleTextStyle': {
                                        color: '#000000',
                                        bold: true,
                                      },
                                      'textStyle':{color: '#000000'},
                                    },
                                    vAxis: {
                                      'textPosition': 'none',
                                      'titleTextStyle': {
                                        color: '#000000',
                                        bold: true
                                      },
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
                              titleTextStyle: {
                                color: '#000000',
                                bold: true
                              },
                              textStyle:{color: '#000000'}
                            },
                            'vAxis': {
                              title: 'Price',
                              titleTextStyle: {
                                color: '#000000',
                                bold: true
                              },
                              format: 'currency',
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

                function drawReturnChart(range_start, range_end){
                    chart_title = document.getElementById('chart_title');
                    chart_title.innerHTML = 'Return Chart ' + symbol_list;

                    data = buildReturnDataTable(range_start);
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
                                      'titleTextStyle': {
                                        color: '#000000',
                                        bold: true
                                      },
                                      'textStyle':{color: '#000000'},
                                    },
                                    vAxis: {
                                      'textPosition': 'none',
                                      'titleTextStyle': {
                                        color: '#000000',
                                        bold: true
                                      },
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
                            'hAxis': {
                              title: 'Date',
                              titleTextStyle: {
                                color: '#000000',
                                bold: true
                              },
                              textStyle:{color: '#000000'}
                            },
                            'vAxis': {
                              title: 'Return %',
                              titleTextStyle: {
                                color: '#000000',
                                bold: true
                              },
                              format: 'percent',
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
                    google.visualization.events.addListener(control, 'statechange', function (e) {
                        var v = control.getState();
                        this.range_start = v.range.start;
                        this.range_end = v.range.end;
                        if (!e.inProgress){
                            data = buildReturnDataTable(this.range_start);
                            dash.draw(data);
                        }
                    });
                }

                function getStartDatePos(start_date){
                    for (i=0; i < date_list.length; i++){
                        var next_date = new Date(date_list[i]);
                        if (next_date == start_date)
                            return i;
                    }
                    return 0;
                }

                function getNewDateList(start_date, end_date, start_date_pos){
                    new_date_list = [];
                    for (i=start_date_pos; i < date_list.length; i++){
                        var next_date = new Date(date_list[i]);
                        if (next_date >= start_date && next_date <= end_date){
                            new_date_list.push(next_date);
                        }
                    }

                    return new_date_list;
                }

                function buildReturnDataTable(start_date){
                    var data_table = new google.visualization.DataTable();
                    data_table.addColumn('date', 'Date');

                    symbol_num = 0
                    symbol_incr = []
                    for (k = 0; k < symbol_list.length; k++){
                        symbol = symbol_list[k];
                        symbol_incr[symbol_num] = 0;
                        data_table.addColumn('number', symbol);
                        symbol_num++;
                    }

                    for (i = 0; i < date_list.length; i++){
                        var cur_date = new Date(date_list[i]);
                        data_list = [cur_date];
                        symbol_num = 0
                        for (k = 0; k < symbol_list.length; k++){
                            j = symbol_incr[symbol_num];
                            if (cur_date.getTime() <= start_date){
                                data_list.push(0);
                                symbol_incr[symbol_num]++;
                            }
                            else{
                                symbol = symbol_list[k];
                                quotes = dict_quotes[symbol];
                                var quote_date = new Date(quotes[j][0]);
                                if (quote_date.getTime() == cur_date.getTime()){
                                    var ret = parseFloat(quotes[j][2]);
                                    if (isNaN(ret)){
                                        if (j > 0)
                                            data_list.push(data_table.getValue(j - 1, symbol_num + 1));
                                        else
                                            data_list.push(0);
                                    }
                                    else if (j > 0)
                                        data_list.push(data_table.getValue(j - 1, symbol_num + 1) + ret);
                                    else
                                        data_list.push(ret);

                                    symbol_incr[symbol_num]++;
                                }
                                else{
                                    if (j > 0)
                                        data_list.push(data_table.getValue(j - 1, symbol_num + 1));
                                    else
                                        data_list.push(0);
                                }
                            }
                            symbol_num++;
                        }
                        data_table.addRow(data_list);
                    }

                    return data_table;
                }

                function drawChart(){
                    if (this.symbol == null)
                        this.symbol = Object.keys(dict_quotes)[0];
                    symbol = this.symbol;

                    loadPriceChart(symbol);
                }

                $(document).ready( function () {
                        var top_table = $('#top_list_table_id').DataTable({
                            select: {
                                style: "os"
                            },
                            scrollY: '50vh',
                            scrollCollapse: true,
                            "order": [[ 2, "desc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ],
                            responsive: true,
                            columnDefs: [
                                { responsivePriority: 1, targets: 0 },
                                { responsivePriority: 2, type : "num", targets: -1 }
                            ]
                        });
                        var bottom_table = $('#bottom_list_table_id').DataTable({
                            select: {
                                style: "os"
                            },
                            scrollY: '50vh',
                            scrollCollapse: true,
                            "order": [[ 2, "asc" ]],
                            "lengthMenu": [ [-1, 5, 10, 20], ["All", 5, 10, 20] ],
                            responsive: true,
                            columnDefs: [
                                { responsivePriority: 1, targets: 0 },
                                { responsivePriority: 2, type : "num", targets: -1 }
                            ]
                        });

                        top_table.on( 'select', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = top_table.rows( indexes ).data().pluck( 0 );

                                for (i = 0; i < data.length; i ++){
                                    if (symbol_list.indexOf(data[i]) == -1)
                                        symbol_list.push(data[i]);
                                }
                                if (symbol_list.length > 1)
                                    loadReturnChart();
                                else
                                    loadPriceChart(data[0]);
                            }
                        } );
                        top_table.on( 'deselect', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = top_table.rows( indexes ).data().pluck( 0 );

                                for (i = 0; i < data.length; i ++){
                                    index = symbol_list.indexOf(data[i]);
                                    if (index != -1)
                                        symbol_list.splice(index,1);
                                }

                                if (symbol_list.length > 1)
                                    loadReturnChart();
                                else if (symbol_list.length == 1)
                                    loadPriceChart(symbol_list[0]);
                                else
                                    loadPriceChart(data[0]);
                            }
                        } );

                        bottom_table.on( 'select', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = bottom_table.rows( indexes ).data().pluck( 0 );

                                for (i = 0; i < data.length; i ++){
                                    if (symbol_list.indexOf(data[i]) == -1)
                                        symbol_list.push(data[i]);
                                }
                                if (symbol_list.length > 1)
                                    loadReturnChart();
                                else
                                    loadPriceChart(data[0]);
                            }
                        } );
                        bottom_table.on( 'deselect', function ( e, dt, type, indexes ) {
                            if ( type === 'row' ) {
                                var data = bottom_table.rows( indexes ).data().pluck( 0 );

                                for (i = 0; i < data.length; i ++){
                                    index = symbol_list.indexOf(data[i]);
                                    if (index != -1)
                                        symbol_list.splice(index,1);
                                }

                                if (symbol_list.length > 1)
                                    loadReturnChart();
                                else if (symbol_list.length == 1)
                                    loadPriceChart(symbol_list[0]);
                                else
                                    loadPriceChart(data[0]);
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
                        if (symbol_list.length > 1)
                            loadReturnChart();
                        else
                            drawChart();
                    });

                    function loadPriceChart(symbol){
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
				                if (isNaN(quote))
				                    quote = prevQuote;
				                else{
				                    // Back-fill previous values if this is the first valid quote
				                    if (prevQuote == 0){
				                        for (k=0; k < i; k++){
				                            var back_item = []
				                            back_item[0] = new Date(date_list[k]);
				                            back_item[1] = quote;
				                            chart_array[k] = back_item;
				                        }
				                    }
    				                prevQuote = quote;
                                }
				                j++;
				            }
                            var item = [];
                            item[0] = next_expected_date;
                            item[1] = quote;
                            chart_array[i] = item;
                        }

                        var start_date = new Date('2015-12-31');
                        var end_date = new Date('2016-09-23');
                        if (this.range_start != null){
                            start_date = this.range_start;
                        }

                        if (this.range_end != null){
                            end_date = this.range_end;
                        }

                        drawPriceChart(symbol, start_date, end_date);
                    }

                    function loadReturnChart(){
                        var start_date = new Date('2015-12-31');
                        var end_date = new Date('2016-09-23');
                        if (this.range_start != null){
                            start_date = this.range_start;
                        }

                        if (this.range_end != null){
                            end_date = this.range_end;
                        }

                        drawReturnChart(start_date, end_date);
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
