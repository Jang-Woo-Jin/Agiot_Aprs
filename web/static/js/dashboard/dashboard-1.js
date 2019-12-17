function doStuff() {
    console.log("Irrigation Switch!")
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

window.onload = function () {

    var dataPoints = [];

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2",
        title: {
            text: "Soil Moisture"
        },
        axisY: {
            title: "%",
            titleFontSize: 15
        },
        data: [{
            type: "column",
            yValueFormatString: "## %",
            dataPoints: dataPoints
        }]
    });

    function addData(data) {
        for (var i = 0; i < data.length; i++) {
            dataPoints.push({
                x: new Date(data[i].s_datetime),
                y: data[i].soil_moisture
            });
        }
        chart.render();
    }

    var farmID = document.getElementById("farm_id").innerHTML;
    console.log(farmID)
    $.ajax({
        type: "GET",
        url: "/api/farm/get/soil-moisture",
        data: {
            farm_id: farmID,
        },
        success: function (data) {
            console.log(data['soil_moisture']);
            addData(data['soil_moisture']);
        },
    })
}
