Chart.defaults.global.defaultFontFamily = "'Nanum Gothic','Georgia', 'serif'"

const truncateSize = 10;    // if label's size is bigger then this size, truncate label
const cutoutPercentage = 65;    // ratio for doughnut chart's width
const chartLabelFontSize = 10;
const chartLabelFontColor = '#BBBBBB';
const barChartColors = ['#5195f3'];

window.onload = function () {
    var farmID = $("#farm_id").attr('value');
    console.log(farmID);

    initSoilChart();
}

function doStuff() {
    console.log("Irrigation Switch!");
}

function toggle(button, farmID) {
    console.log("TOGGLE")
    console.log("FARMID : ", farmID)
    if (button.value == "OFF") {
        button.value = "ON"
        button.innerHTML = "ON"
        this.interval = setInterval(doStuff, 1000);
        $.ajax({
            url: "/farm/actuator",
            method: "POST",
            data: {
                result: "on",
                farm_id: farmID
            },
            success: function (data) {
                if (data['success'] == true) {
                    if (!alert('Actuator Turned On')) {
                        window.location.reload();
                    }
                }
                if (data['success'] == false) {
                    if (!alert("Actuator Failed to Turn on")) {
                        window.location.reload();
                    }
                }
            },
            error: function () {
                alert("Actuator Failed to Turn on");
            }
        })
    } else if (button.value == "ON") {
        button.value = "OFF"
        button.innerHTML = "OFF"
        $.ajax({
            url: "/farm/actuator",
            method: "POST",
            data: {
                result: "off",
                farm_id: farmID
            },
            success: function (data) {
                if (data['success'] == true) {
                    if (!alert('Actuator Turned Off')) {
                        window.location.reload();
                    }
                }
                if (data['success'] == false) {
                    if (!alert("Actuator Failed to Turn Off")) {
                        window.location.reload();
                    }
                }
            },
            error: function () {
                alert("Actuator Failed to Turn Off");
            }
        });
    }
}

function initSoilChart() {
    $.ajax({
        type: 'GET',
        url: '/api/farm/get/soil-moisture',

        success: function (data) {
            console.log(data)
            makeBarChart($("#soil_chart"), data)
        },
        error: function () {
            console.log("Error : can't get soil chart data");
        }
    });
}

function makeBarChart(chartObj, chartData) {
    let barChartData = makeBarChartData(chartData);
    let barChartFormat = addBarChartOptions(barChartData);

    let chartOptions = {
        type: 'bar',
        chartObj: chartObj,
        data: barChartFormat
    };
    drawChart(chartOptions);
}

/* make specific data - depending on each elements, it choose and serialized called data */
function makeBarChartData(chartData) {
    let labels = [];
    let value = [];

    let data = {
        labels: chartData.index,//labels,
        data: chartData.data,//value,
        colors: barChartColors
    }

    return data;
}

function addBarChartOptions(data) {
    let barChartData = {
        labels: data.labels,    // set chart label data
        datasets: [{
            data: data.data,    // set chart value data
            backgroundColor: data.colors[0],    // set chart color
            borderColor: data.colors[0],        // set chart border color
            borderWidth: 1,                     // set chart border width
            hoverBorderWidth: 3                 // set chart border width when hover some chart data
        }],
        // options for legend
        legend: {
            display: false      // hide chart legend
        },
        // options for x, y axes
        scales: {
            xAxes: [{
                ticks: {
                    fontColor: chartLabelFontColor,
                    fontSize: chartLabelFontSize
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Time',      // label string for x axis
                    fontColor: chartLabelFontColor,
                    fontSize: chartLabelFontSize
                }
            }],
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,      // y axis is started with 0
                    fontColor: chartLabelFontColor,
                    fontSize: chartLabelFontSize,
                    callback: function (value) {
                        if (value % 1 === 0) {
                            return value;
                        }
                    }    // remove real value for show only integer value
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Soil Moisture',    // label string for y axes
                    fontColor: chartLabelFontColor,
                    fontSize: chartLabelFontSize
                }
            }]
        }
    };

    return barChartData;
}

/* draw and update chart */
function drawChart(options) {
    let type = options.type;
    let chartObj = options.chartObj;
    let data = options.data;

    // if chart's all data is 0, it shows no data text
    if (isAllZero(data.datasets) && type != 'bar') {
        let chart = chartObj.data('chart');
        // if chart is already exist, it updates the chart - it has no data that it removes the chart
        if (chart != undefined) {
            updateChart(chart, data);
        }
    } else {
        let chart = chartObj.data('chart');
        // if chart is already exist, it updates the chart
        if (chart != undefined) {
            updateChart(chart, data);
        } else {
            let windowWidth = $(window).width();

            let chart = new Chart(chartObj, {
                type: type,
                data: {
                    datasets: data.datasets,
                    labels: truncateLabel(data.labels, truncateSize)
                },
                options: {
                    legend: data.legend,
                    cutoutPercentage: cutoutPercentage,     // it used for doughnut chart
                    maintainAspectRatio: false,     // if it is true, maintain the original canvas width and height ratio when resizing
                    scales: data.scales !== undefined ? data.scales : null,
                    tooltips: {
                        callbacks: {
                            label: function (t, d) {
                                let xLabel = data.labels[t.index],
                                    yLabel = d.datasets[t.datasetIndex].data[t.index];
                                return xLabel + ': ' + yLabel;
                            }
                        }
                    }
                }
            });
            chartObj.data('chart', chart);
        }
    }
}

function updateChart(chart, datas) {
    let i = 0;
    chart.data.datasets.forEach(function (dataset) {
        dataset.data = datas.datasets[i++].data;
    });
    chart.data.labels = truncateLabel(datas.labels, 10);
    chart.options.tooltips.callbacks = {
        label: function (t, d) {
            let xLabel = datas.labels[t.index],
                yLabel = d.datasets[t.datasetIndex].data[t.index];
            return xLabel + ': ' + yLabel;
        }
    }
    chart.update();
}

/* some util functions */
function calPreMonth(today, month) {
    let split = today.split('-');
    return split[0] + '-' + pad((split[1] - month), 2) + '-' + split[2];
}

function pad(n, width) {
    n = n + '';
    return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
}

function isAllZero(datasets) {
    let isAllZero = true;

    datasets.forEach(function (dataset) {
        dataset.data.some(function (elements) {
            if (elements != 0) isAllZero = false;
            return elements != 0;
        });
        if (!isAllZero) return;
    });

    return isAllZero;
}

function truncateLabel(label, size) {
    let trunc_label = [];
    label.forEach(function (data) {
        if (data.length > size) {
            data = data.substring(0, size - 3) + '...'
        }
        trunc_label.push(data);
    });
    return trunc_label;
}