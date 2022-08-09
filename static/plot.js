var graph = document.getElementById("graph");
let data = [{ // Data points
        x: [],
        y: [],
        mode: 'markers',
        marker: {color: 'black', size: 3},
        xaxis:{type: 'date'}
    },
    {  // Endpoints of regression line
        x: [],
        y: [],
        mode: 'lines',
        marker: {color: 'blue', size:1},
        line: {width: 1},
        opacity: 0.3
    },
    {   // Trace for calculated points
           x:[],
           y:[],
           yaxis: 'y2',

           // plotcolor: ['green'],
           mode: 'lines',
           marker: {color: 'green'},
           line: {width: 2},
           opacity: 0.6
    }];
// This array of empty traces is used whenever we need to restart a plot after it has been stopped.
// Since the array is empty, the restarted plot will start with no data.
let initData = [{ // Data points
        x: [],
        y: [],
        mode: 'markers',
        marker: {color: 'black', size: 3},
        xaxis:{type: 'date'}
    },
    {  // Endpoints of regression line
        x: [],
        y: [],
        mode: 'lines',
        marker: {color: 'blue', size:1},
        line: {width: 1},
        opacity: 0.3
    },
    {   // Trace for calculated points
           x:[],
           y:[],
           yaxis: 'y2',

           plotcolor: ['green'],
           mode: 'lines',
           marker: {color: 'green'},
           line: {width: 2},
           opacity: 0.6
    }];
    let layout = {
        margin: {t:100},
        xaxis: {type: 'date'},
        yaxis: {range: [0, 1],
                title: 'Pump Pressure',
                side: 'left'},
        yaxis2: {title: 'Percent Diff From Regression Line',
                 titlefont: {color: 'green'},
                 overlaying: 'y',
                 side: 'right',
                 range: [-100, 100],
                 zerolinecolor: 'green'
        },
        showlegend: false

    };

// First do a deep clone of the data array of traces.  The clone uses values from the empty array, initData
// Then call Plotly.newPlot() using the cloned array of empty traces to start a new plot.
function initPlot(rangeData){
    let rangeJsonObj = JSON.parse(rangeData);
    data[0].x = Array.from(initData[0].x);
    data[0].y = Array.from(initData[0].y);
    data[1].x = Array.from(initData[1].x);
    data[1].y = Array.from(initData[1].y);
    data[2].x = Array.from(initData[2].x);
    data[2].y = Array.from(initData[2].y);
    let yAxis = layout.yaxis
    yAxis.range = rangeJsonObj.range;
    Plotly.newPlot('graph', data, layout);
}

var msgCounter = 0; // Another way of shifting. Not used in this code.

function updatePlot(jsonData){
    //console.log("plot.js updatePlot()  " + jsonData);
    //console.log("msgCounter: " + msgCounter++);
    let jsonObj = JSON.parse(jsonData); 
    // jsonObj is in the form:
     // {'plotpoint': [timestamp, sensor_val],
     //    'regress': {'xs': [x1, x2],
     //                'ys': [y1, y2]
     //                },
     //    'calc': {'x1': x_old_p,
     //             'x2': x_new_p,
     //             'y_diff1': y_percent_diff_old,
     //             'y_diff2': y_percent_diff,
     //             'plot_color': plot_color,
      //            'row_counter': row_counter
      //            'max_window_size': max_window_size
      //            }
     //  }

    let timestamp = jsonObj.plotpoint[0];
    let sensorValue = jsonObj.plotpoint[1];

    let regress = jsonObj.regress;
    let x1 = regress.xs[0];
    let x2 = regress.xs[1];
    let y1 = regress.ys[0];
    let y2 = regress.ys[1];
    let diffNode = jsonObj.calc;
    let diff_x1 = diffNode.x1;
    let diff_x2 = diffNode.x2;
    let diff_y1 = diffNode.y_diff1;
    let diff_y2 = diffNode.y_diff2;
    // Next two values would be used to change the plot color in real time, but Plotly.js does not support
    let plot_color = diffNode.plot_color;
    let row_counter = diffNode.row_counter;

    let max = diffNode.max_window_size;

    // Add new data point as well as calculated data for regression line start and end points as well as the
    // y difference plot.  Note there are three traces.  The first two traces use the same layout named yaxis.
    // The third trace uses the layout named yaxis2.  This naming convention follows that of plotly.js
    Plotly.extendTraces('graph', {
        // NOTE:  The below 2 commented lines would be used if the dynamic line coloring were supported by plotly.js
        //x: [[timestamp], [x1, x2], [diff_x1, diff_x2]],
        //y: [[sensorValue], [y1,y2], [diff_y1, diff_y2]]
        x: [[timestamp], [x1, x2], [diff_x2]],
        y: [[sensorValue], [y1,y2], [diff_y2]]

    }, [0, 1, 2], max);  // The array denotes to plot all three traces(0 based).  Keep only last max data points


    // NOTE:  This code below was an attempt to dynamically change the color of the Percent Diff plot to red whenever
    // the plot went beyond the acceptable range.  Plotly.js does not support such a feature.

    //if(plot_color != null){
    //    let updateStr = 'marker.color[' + row_counter + ']';
        //Plotly.restyle('graph', editObj, [2]);
    //    Plotly.react(graph, {[updateStr]: plot_color}, null, [2]);

    //}

}