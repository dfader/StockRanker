var previousDayVolumeArray = [[],[2]];
var todayDayVolumeArray=[[],[]];
var predictArray = [];
var currentDateTime = new Date('2016-07-26T09:48:00-0400');
var rangeStart;
// var currentDateTime = new Date();

function getCurrentDateTime(){
	currentDateTime = new Date(currentDateTime.getTime() +  1*60000); 
	return currentDateTime;
}

google.charts.load('visualization', '1', {packages: ['controls', 'charteditor', 'corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawPriceChart(stopPoint, rangeStart, rangeEnd){
    var data = new google.visualization.DataTable();
	var nStop = 2;
	var j=0;
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
					  'titleTextStyle': {color: '#FFFFFF'},
					  'textStyle':{color: '#FFFF00'},
					},
					vAxis: {
					  'textPosition': 'none',
					  'titleTextStyle': {color: '#FFFFFF'},
					  'textStyle':{color: '#FFFF00'},
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
			'colors': ['#e2431e', '#66ff66'],
			'hAxis': {
			  title: 'Time',
			  titleTextStyle: {color: '#FFFFFF'},
			  textStyle:{color: '#FFFF00'}
			},
			'vAxis': {
			  title: 'Trade volume',
			  titleTextStyle: {color: '#FFFFFF'},
			  textStyle:{color: '#FFFF00'}
			},
			legend: {
				textStyle: {color: 'white'},
				position: 'top'
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

function testRefresh(){
	console.log("refreshed!");
	// console.log(getCurrentDateTime());
		//var rangeStart = '2016-07-26T10:00:00-0400';
		// var rangeEnd = '2016-07-26T10:10:00-0400';
		var d = getCurrentDateTime();
		console.log(d.value);
		var requestDate = getDateString(d);

		var minute = d.getMinutes();
		var hour = d.getHours();
		var currentPoint = (hour-9)*60 + (minute - 30);
		$.get("https://localhost:9000/predict", {date: requestDate}, function(data, status){
		
			$("#cashtag").html("new Value: "+ data);
			predictArray.shift();
			predictArray.push(parseInt(data));
		});
		
		// var d = new Date('2016-07-26T11:30:00-0400');
		// var minute = d.getMinutes();
		// var hour = d.getHours();
		// var currentPoint = (hour-9)*60 + (minute - 30);
		if(this.rangeStart!=null){
			// rangeEnd = new Date(rangeEnd
			var rangeEnd   = d.getTime() + 3*60000;
			drawPriceChart(currentPoint, this.rangeStart, rangeEnd);
		}else{
			var rangeStart = d.getTime() - 30*60000;
			var rangeEnd   = d.getTime() + 3*60000;
			drawPriceChart(currentPoint, rangeStart, rangeEnd);
		}
	
}


function drawChart() {
		// var rangeStart = '2016-07-26T10:00:00-0400';
		// var rangeEnd = '2016-07-26T10:10:00-0400';
		// var stopPoint = "2";
		// var d = getCurrentDateTime();
		// console.log(d.value);
		// var requestDate = d.getFullYear()+"." + (d.getMonth() +1)+"." + d.getDay()+ "." + d.getHours()+ "."+ d.getMinutes();

		// var minute = d.getMinutes();
		// var hour = d.getHours();
		// var currentPoint = (hour-9)*60 + (minute - 30);
		// var rangeStart = d.getTime() - 3*60000
		// var rangeEnd   = d.getTime() + 3*60000

		// drawPriceChart(currentPoint, rangeStart, rangeEnd);
		
		///////////////////////////

	setInterval(testRefresh, 5000); 
	setInterval(updateTable, 5000); 


    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Time of Day');
    data.addColumn('number', 'Previous Day trade volume');

    for (var i = 0; i < 391; i++) {
        data.addRow([previousDayVolumeArray[i][0],previousDayVolumeArray[i][1]]);
    }
      var options = {
		backgroundColor: { fill:'transparent' },
		animation: {
			startup: true,
			duration: 5000, 
			easing: 'inAndOut'
		},
        hAxis: {
          title: 'Time',
		  titleTextStyle: {color: '#FFFFFF'},
		  textStyle:{color: '#FFFF00'}
        },
        vAxis: {
          title: 'Trade volume',
		  titleTextStyle: {color: '#FFFFFF'},
		  textStyle:{color: '#FFFF00'}
        },
		//legend: 'top',
		legend: {
			textStyle: {color: 'white'},
			position: 'top'
		}
      };

      var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

      chart.draw(data, options);    
    
    // var dash = new google.visualization.Dashboard(document.getElementById('dashboard'));

    // var control = new google.visualization.ControlWrapper({
        // 'controlType': 'ChartRangeFilter',
        // 'containerId': 'control_div',
        // 'options': {
            // 'filterColumnIndex': 0,
            // 'ui': {
                // 'chartOptions': {
                    // height: 30,
                    // width: '100%',
                    // chartArea: {
                        // width: '80%'
                    // }
                // },
				// snapToData: true,
                // chartView: {
                    // columns: [0,1]
                // }
            // }
        // },
		// 'state':{
			// 'range': {
				// 'start': new Date('2016-07-25T10:30:00-0400'),
				// 'end': new Date('2016-07-25T11:50:00-0400')
			// }
		// }
    // });

    // var chart = new google.visualization.ChartWrapper({
        // chartType: 'LineChart',
        // containerId: 'chart_div',
 		// 'options':{
			// 'legend': {position: 'top', alignment: 'start'}
		// }
   // });

    // function setOptions (wrapper) {
       
        // wrapper.setOption('width', '100%');
        // wrapper.setOption('chartArea.width', '80%');
		// // wrapper.setOption('legend': {position: 'top', alignment: 'start'});

      
    // }
    
    // setOptions(chart);
   
    
    // dash.bind([control], [chart]);
    // dash.draw(data);
  	// google.visualization.events.addListener(control, 'statechange', function () {
        // var v = control.getState();
        // document.getElementById('dbgchart').innerHTML = v.range.start+ ' to ' +v.range.end;
        // return 0;
    // });
}



$(document).ready(function(){
		console.log("Volume call for previous day");
		console.log(new Date());
        $.get("https://localhost:9000/volume", {ticker: "AAPL", date: "2016.07.25"}, function(data, status){
			var startDate = new Date('2016-07-25T09:30:00-0400');
			console.log(startDate)
			var volumeArray = data;
			var length = volumeArray.length;
			for(i=0; i<length; i++){
				var newDate = new Date(startDate.getTime() + i*60000);
				var item = [];
				// item[0] = [newDate.getHours(), newDate.getMinutes()];
				item[0] = newDate;
				item[1] =volumeArray[i];
				previousDayVolumeArray[i] = item;
			}
        });

		console.log("Volume call for current day");
        $.get("https://localhost:9000/volume", {ticker: "AAPL", date: "2016.07.26"}, function(data, status){
			var startDate = new Date('2016-07-26T09:30:00-0400');
			console.log(startDate)
			var volumeArray = data;
			var length = volumeArray.length;
			for(i=0; i<length; i++){
				var newDate = new Date(startDate.getTime() + i*60000);
				var item = [];
				// item[0] = [newDate.getHours(), newDate.getMinutes()];
				item[0] = newDate;
				item[1] =volumeArray[i];
				todayDayVolumeArray[i] = item;
			}
			
			console.log("predict call for first minute");


			// var d = new Date('2016-07-26T11:30:00-0400');
			var d = new Date();
			d.setDate(d.getDate()-1);
			var requestDate = getDateString(d);
			$.get("https://localhost:9000/predict", {date: requestDate}, function(data, status){
			
				$("#cashtag").html("new Value: "+ data);
			
				predictArray.push(parseInt(data));
				
				console.log("predict call for second minute");
				var origDate = new Date();
				origDate.setDate(origDate.getDate()-1);
				var d = new Date(origDate.getTime() + 1*60000);
				var requestDate = getDateString(d);
				$.get("https://localhost:9000/predict", {date: requestDate}, function(data, status){
				
					$("#cashtag").html("new Value: "+ data);
				
					predictArray.push(parseInt(data));

					// console.log("predict call for third minute");
					// var origDate = new Date();
					// var d = new Date(origDate.getTime() + 2*60000);
					// var requestDate = d.getFullYear()+"." + (d.getMonth() +1)+"." + d.getDay()+ "." + d.getHours()+ "."+ d.getMinutes();

					// $.get("https://localhost:9000/predict", {date: requestDate}, function(data, status){
					
						// $("#cashtag").html("new Value: "+ data);
					
						// predictArray.push(parseInt(data));

						var d = getCurrentDateTime();
						console.log(d.value);
						var requestDate = getDateString(d);
						var minute = d.getMinutes();
						var hour = d.getHours();
						var currentPoint = (hour-9)*60 + (minute - 30);
						var rangeStart = d.getTime() - 30*60000
						var rangeEnd   = d.getTime() + 3*60000

						 drawPriceChart(currentPoint, rangeStart, rangeEnd);
										
					// });	
				});
			});
		});
        if (window.location.search && /cashtag/.test(window.location.search)) {
        	var href = window.location.search;
        	var symbol = href.substring(href.indexOf("cashtag") + 11, href.indexOf("&"));
        	var searchInput = document.getElementById('searchBar');
        	searchInput.value = symbol;
        }
        
        updateTable();
});


function getDateString(d){
	return d.getFullYear()+"." + ("0" + (d.getMonth() +1)).slice(-2) +"." + ("0" + d.getDate()).slice(-2) + "." + ("0" + d.getHours()).slice(-2) + "."+ ("0" + d.getMinutes()).slice(-2);
}

function updateTable(){
	 xhrGet("https://localhost:9000/performance", function(responseText){
		 	var performanceDiv = document.getElementById('performanceDiv');
		 	performanceDiv.innerHTML = buildTable(responseText);
    }, function(err){
    	console.log(err);
    });
}



function buildTable(array){
	var array = JSON.parse(array);
	
	var tableDiv = "<table id=\"perfTable\" class=\"perf\">" +
				"<thead>" + 
				"<th style='width:10%'> BasketID </th>" +
				"<th style='width:5%'> TtlShares </th>" +
				"<th style='width:5%'> % Sent </th>" +
				"<th style='width:5%'> % Exec </th>" +
				"<th style='width:5%'> Status </th>" +
				"<th style='width:5%'> Real. P&L </th>" +
				"<th style='width:5%'> Unreal. P&L </th>" +
				"<th style='width:5%'> vs Arrival (bps) </th>" +
				"<th style='width:5%'> vs Open (bps) </th>" +
				"<th style='width:5%'> vs PDC (bps) </th>" +
				"<th style='width:5%'> vs VWAP (bps) </th>" +
				"</thead><tbody>";
	
	for (i = 0; i < array.length; i++) {
		var obj = array[i];
		var total = obj.total;
		var sent = obj.sent;
		var exec = obj.exec;
		var status = obj.status;
		var realPL = obj.realPL;
		var unrealPL = obj.unrealPL;
		var arrival = obj.arrival;
		var open = obj.open;
		var pdc = obj.pdc;
		var vwap = obj.vwap;
		
		if (total.indexOf(".") > 0){
			total = total.slice(0, total.indexOf("."))
		}
		
		if (sent.indexOf(".") > 0){
			sent = sent.slice(0, sent.indexOf("."))
		}
		
		if (exec.indexOf(".") > 0){
			exec = exec.slice(0, exec.indexOf("."))
		}
		
		if (realPL.indexOf(".") > 0 && (realPL.length - 2) > realPL.indexOf(".")){
			realPL = realPL.slice(0, realPL.indexOf(".") + 2)
		}
		
		if (unrealPL.indexOf(".") > 0 && (unrealPL.length - 2) > unrealPL.indexOf(".")){
			unrealPL = unrealPL.slice(0, unrealPL.indexOf(".") + 2)
		}
		
		if (arrival.indexOf(".") > 0 && (arrival.length - 2) > arrival.indexOf(".")){
			arrival = arrival.slice(0, arrival.indexOf(".") + 2)
		}
		
		if (open.indexOf(".") > 0 && (open.length - 2) > open.indexOf(".")){
			open = open.slice(0, open.indexOf(".") + 2)
		}
		
		if (pdc.indexOf(".") > 0 && (pdc.length - 2) > pdc.indexOf(".")){
			pdc = pdc.slice(0, pdc.indexOf(".") + 2)
		}
		

		if (vwap.indexOf(".") > 0 && (vwap.length - 2) > vwap.indexOf(".")){
			vwap = vwap.slice(0, vwap.indexOf(".") + 2)
		}
		
		var row = "<tr><td>" + obj.id + 
					"</td><td>" + total +
					"</td><td>" + sent +
					"</td><td>" + exec +
					"</td><td>" + status +
					"</td><td>" + realPL +
					"</td><td>" + unrealPL +
					"</td><td>" + arrival +
					"</td><td>" + open +
					"</td><td>" + pdc +
					"</td><td>" + vwap +
					"</td></tr>";  
		tableDiv += row;
	}
	tableDiv += "</tbody></table>";
	
	return tableDiv;
}

