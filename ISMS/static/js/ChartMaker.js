function makeConfig(passed_canvas, labels, data, data_label, title) {
    let delayed;
    let gradient = passed_canvas.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, "#bbf7d0");
    gradient.addColorStop(0.25, "#86efac");
    gradient.addColorStop(0.5, "#4ade80");
    gradient.addColorStop(0.75, "#22c55e");
    gradient.addColorStop(1, "#16a34a");
    config = {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: null, // Need to Chane
                data: null, // Need to Chane
                fill: true,
                backgroundColor: gradient,
                pointBackgroundColor: "#64748b",
                tension: 0.5
            }]
        },
        options: {
            title:{
                display: true,
                text: null, // Need to Chane
                fontSize: 25
            },
            legend:{
                display: true,
                position: "top"
            },
            tooltips:{
                enabled: true
            },
            radius:4,
            hitRadius: 20,
            hoverRadius: 6,
            responsive: true,
            animation: {
                onComplete: () => {
                  delayed = true;
                },
                delay: (context) => {
                  let delay = 0;
                  if (context.type === 'data' && context.mode === 'default' && !delayed) {
                    delay = context.dataIndex * 300 + context.datasetIndex * 100;
                  }
                  return delay;
                },
            },
            scales: {
                x :{
                    type: "time",
                    time: {
                        unit: "minute"
                    }
                },
            },
            maintainAspectRatio: false
        }
    }
    if (Array.isArray(data[0])) {
        config.data.datasets = []
        data.forEach((dataset, index) => {
            config.data.datasets.push({
                label: data_label[index],
                data: dataset,
                fill: true,
                backgroundColor: gradient,
                pointBackgroundColor: "#64748b",
                tension: 0.5
            })
        })
    } else {
        config.data.datasets[0].data = data;
        config.data.datasets[0].label = data_label;
    }
    config.data.labels = labels;
    config.options.title.text = title;
    return config
}

const HUD = {
    fromDateTime: document.getElementById("start_date"),
    toDateTime: document.getElementById("end_date"),
    submitBtn : document.getElementById("get-data"),
    addListeners () {
        HUD.submitBtn.addEventListener("click", (e) => {
            e.preventDefault()
            if (HUD.fromDateTime.value === "" || HUD.toDateTime.value === "") {
                alert("Please select a date range")
                return
            }
            GRAPHS.data = GRAPHS.getData(HUD.fromDateTime.value, HUD.toDateTime.value)
        });
    }
}

const GRAPHS = {
    API_URL : "/api/clusters/",
    clusterID: document.URL.split("/")[4],
    latestAPI : `/api/clusters/${document.URL.split("/")[4]}/latest`,
    data: {},
    temperatureCanvas : document.getElementById("temperature-canvas").getContext('2d'),
    humidityCanvas: document.getElementById("humidity-canvas").getContext('2d'),
    pressureCanvas: document.getElementById("pressure-canvas").getContext('2d'),
    mq2LmCanvas: document.getElementById("mq2_lm-canvas").getContext('2d'),
    mq2HsCanvas: document.getElementById("mq2_hs-canvas").getContext('2d'),
    mq135Canvas : document.getElementById("mq135-canvas").getContext('2d'),
    temperatureChart: null,
    humidityChart: null,
    pressureChart: null,
    mq2HsChart: null,
    mq2LmChart: null,
    mq135Chart: null,
    init () {
        GRAPHS.temperatureChart = new Chart(GRAPHS.temperatureCanvas, makeConfig(GRAPHS.temperatureCanvas,GRAPHS.data.date_time, GRAPHS.data.temperature, "Temperature", "Temperature"))
        GRAPHS.humidityChart = new Chart(GRAPHS.humidityCanvas, makeConfig(GRAPHS.humidityCanvas, GRAPHS.data.date_time, GRAPHS.data.humidity, "Humidity", "Humidity"))
        GRAPHS.pressureChart = new Chart(GRAPHS.pressureCanvas, makeConfig(GRAPHS.pressureCanvas, GRAPHS.data.date_time, GRAPHS.data.pressure, "Pressure", "Pressure"))
        GRAPHS.mq2HsChart = new Chart(GRAPHS.mq2HsCanvas, makeConfig(GRAPHS.mq2HsCanvas, GRAPHS.data.date_time, [GRAPHS.data.hydrogen, GRAPHS.data.smoke], ["Hydrogen", "Smoke"], "MQ2_HS"))
        GRAPHS.mq2LmChart = new Chart(GRAPHS.mq2LmCanvas, makeConfig(GRAPHS.mq2LmCanvas, GRAPHS.data.date_time, [GRAPHS.data.lpg, GRAPHS.data.methane], ["Lpg", "Methane"], "MQ2_LM"))
        GRAPHS.mq135Chart = new Chart(GRAPHS.mq135Canvas, makeConfig(GRAPHS.mq135Canvas, GRAPHS.data.date_time, GRAPHS.data.ppm, "MQ135 Air Quality", "MQ135"))
        GRAPHS.fetchUpdates()
    },
    fetchUpdates(){
        setInterval(() => {
            fetch(GRAPHS.latestAPI).then(response => response.json()).then(data => {
                if (data["date_time"] !== GRAPHS.data["date_time"][0]) {
                    for (const param in GRAPHS.data) {
                        GRAPHS.data[param].unshift(data[param])
                        GRAPHS.data[param].pop()    
                    }
                }
            }).then(GRAPHS.updateGraphs())}, 5000)
    },
    updateGraphs(){
        GRAPHS.temperatureChart.update()
        GRAPHS.humidityChart.update()
        GRAPHS.pressureChart.update()
    }
}

async function get_data() {
    await fetch(GRAPHS.API_URL + GRAPHS.clusterID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body:JSON.stringify({
            from:"", to: ""
        })
    }).then(res => res.json()).then(data => {
        GRAPHS.data = data
    })
    return null
}

document.addEventListener("DOMContentLoaded", async () => {
    await get_data();
    HUD.addListeners();
    GRAPHS.init();
})
