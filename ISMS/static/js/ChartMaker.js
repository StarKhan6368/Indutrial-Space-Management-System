function getGradient(passedCanvas, choice) {
    colors = {"green": ["#bbf7d0", "#86efac", "#4ade80", "#22c55e", "#16a34a"],
              "red": ["#f7b6b6", "#f1556c", "#e73d4a", "#c92a2a", "#a61d1d"],
              "blue": ["#144b8e", "#1a60b6", "#2076df", "#498fe5", "#71a8eb"],
              "yellow": ["#f5c00a", "#f7cc37", "#f7cc37", "#f8d763", "#fae290"],
              "purple": ["#7c3b96", "#9848b7", "#aa69c4", "#bd8ad1", "#d0acde"],
              "orange": ["#d16200", "#ff7800", "#ff912e", "#ffa95d", "#ffc28b"]}
    choosenColor = colors[choice]
    const gradient = passedCanvas.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, choosenColor[0]);
    gradient.addColorStop(0.25, choosenColor[1]);
    gradient.addColorStop(0.5, choosenColor[2]);
    gradient.addColorStop(0.75, choosenColor[3]);
    gradient.addColorStop(1, choosenColor[4]);
    return gradient
}

function makeConfig(passedCanvas, labels, data, data_label, title, yAxisLabel, colorChoice, pointColors) {
    let delayed;
    config = {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: null, 
                data: null, 
                fill: true,
                backgroundColor: Array.isArray(colorChoice) ? "" : getGradient(passedCanvas, colorChoice),
                pointBackgroundColor: "#333333",
                tension: 0.5
            }]
        },
        options: {
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
                        unit: "second"
                    }
                },
                y: {
                    ticks: {
                        callback: function(value, index, ticks) {
                            return `${value.toFixed(2)} ${yAxisLabel}`;
                        }
                    }
                }
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
                backgroundColor: getGradient(passedCanvas, colorChoice[index]),
                pointBackgroundColor: pointColors[index],
                tension: 0.5
            })
        })
    } else {
        config.data.datasets[0].data = data;
        config.data.datasets[0].label = data_label;
    }
    config.data.labels = labels;
    return config
}

const HUD = {
    fromDateTime: document.getElementById("start_date"),
    toDateTime: document.getElementById("end_date"),
    submitBtn : document.getElementById("get-data"),
    addListeners () {
        HUD.submitBtn.addEventListener("click", async (e) => {
            e.preventDefault();
            DASH.chartParaDrop.scrollIntoView();
            if (HUD.fromDateTime.value === "" || HUD.toDateTime.value === "") {
                alert("Empty Values, Defaulting to initial range")
                await get_data()
                GRAPHS.updateGraphs()
                GRAPHS.customMode = false
            } else{
                GRAPHS.customMode = true
                await get_data(HUD.fromDateTime.value, HUD.toDateTime.value)
                GRAPHS.updateGraphs()
            }
        });
    }
}

const GRAPHS = {
    API_URL : "/api/clusters/",
    clusterID: document.URL.split("/")[4],
    latestAPI : `/api/clusters/${document.URL.split("/")[4]}/latest`,
    data: {date_time: [], temperature: [], humidity: [], pressure: [], lpg: [], methane: [], hydrogen: [], smoke: [], ppm: []},
    temperatureCanvas : document.getElementById("temperature-canvas").getContext('2d'),
    humidityCanvas: document.getElementById("humidity-canvas").getContext('2d'),
    pressureCanvas: document.getElementById("pressure-canvas").getContext('2d'),
    mq2LmCanvas: document.getElementById("mq2_lm-canvas").getContext('2d'),
    mq2HsCanvas: document.getElementById("mq2_hs-canvas").getContext('2d'),
    mq135Canvas : document.getElementById("mq135-canvas").getContext('2d'),
    selectOption: document.getElementById("x-axis"),
    temperatureChart: null,
    humidityChart: null,
    pressureChart: null,
    mq2HsChart: null,
    mq2LmChart: null,
    mq135Chart: null,
    customMode: false,
    init () {
        GRAPHS.temperatureChart = new Chart(GRAPHS.temperatureCanvas, makeConfig(GRAPHS.temperatureCanvas,GRAPHS.data.date_time, GRAPHS.data.temperature, "Temperature", "Temperature", "°C", "red"))
        GRAPHS.humidityChart = new Chart(GRAPHS.humidityCanvas, makeConfig(GRAPHS.humidityCanvas, GRAPHS.data.date_time, GRAPHS.data.humidity, "Humidity", "Humidity", "%", "green"))
        GRAPHS.pressureChart = new Chart(GRAPHS.pressureCanvas, makeConfig(GRAPHS.pressureCanvas, GRAPHS.data.date_time, GRAPHS.data.pressure, "Pressure", "Pressure", "hPa", "orange"))
        GRAPHS.mq2HsChart = new Chart(GRAPHS.mq2HsCanvas, makeConfig(GRAPHS.mq2HsCanvas, GRAPHS.data.date_time, [GRAPHS.data.methane, GRAPHS.data.smoke], ["Methane", "Smoke"], "MQ2_MS", "PPM", ["blue", "yellow"], ["#FCFAF9", "#333333"]))
        GRAPHS.mq2LmChart = new Chart(GRAPHS.mq2LmCanvas, makeConfig(GRAPHS.mq2LmCanvas, GRAPHS.data.date_time, [GRAPHS.data.lpg, GRAPHS.data.hydrogen], ["Lpg", "Hydrogen"], "MQ2_LH", "PPM", ["blue", "yellow"], ["#FCFAF9", "#333333"]))
        GRAPHS.mq135Chart = new Chart(GRAPHS.mq135Canvas, makeConfig(GRAPHS.mq135Canvas, GRAPHS.data.date_time, GRAPHS.data.ppm, "MQ135 Air Quality", "MQ135", "PPM", "purple"))
        GRAPHS.selectOption.addEventListener("change", () => {
            GRAPHS.temperatureChart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            GRAPHS.humidityChart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            GRAPHS.pressureChart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            GRAPHS.mq2HsChart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            GRAPHS.mq2LmChart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            GRAPHS.mq135Chart.config._config.options.scales.x.time.unit = GRAPHS.selectOption.value
            DASH.chartParaDrop.scrollIntoView();
            GRAPHS.updateGraphs();
        })
    },
    fetchUpdates(data){
        if (new Date(data["date_time"]) > new Date(GRAPHS.data["date_time"][0]) && GRAPHS.customMode === false) {
            for (const param in GRAPHS.data) {
                GRAPHS.data[param].unshift(data[param])
                if (GRAPHS.data.temperature.length > 30) {
                    GRAPHS.data[param].pop()
                }
            }
            GRAPHS.updateGraphs()
        }
    },
    updateGraphs(){
        GRAPHS.temperatureChart.update()
        GRAPHS.humidityChart.update()
        GRAPHS.pressureChart.update()
        GRAPHS.mq2HsChart.update()
        GRAPHS.mq2LmChart.update()
        GRAPHS.mq135Chart.update()
    }
}

function clearData() {
    parametes = Object.keys(GRAPHS.data).map((key) => String(key))
    parametes.forEach((param) => {
        GRAPHS.data[param].splice(0, GRAPHS.data[param].length)
    })
}
async function get_data(from="", to="") {
    await fetch(GRAPHS.API_URL + GRAPHS.clusterID, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        body:JSON.stringify({
            from, to
        })
    }).then(res => res.json()).then(data => {
        clearData()
        for (const param in data) {
            GRAPHS.data[param].push(...data[param])
        }
    })
}

document.addEventListener("DOMContentLoaded", async () => {
    await get_data();
    HUD.addListeners();
    GRAPHS.init();
})
