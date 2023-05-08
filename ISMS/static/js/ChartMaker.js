const GRAPH = {
    API_URL : "/api/clusters/",
    clusterID: document.URL.split("/")[4],
    thresholdAPI : "/api/thresholds",
    thresholds : {},
    data: {},
    fromDateTime: document.getElementById("start_date"),
    toDateTime: document.getElementById("end_date"),
    submitBtn : document.getElementById("get-data"),
    tempChart : document.getElementById("temperature"),
    humidityChart: document.getElementById("humidity"),
    pressureChart: document.getElementById("humidity"),
    mq2LmChart: document.getElementById("mq2_lm"),
    mq2HsChart: document.getElementById("mq2_hs"),
    mq135Chart : document.getElementById("mq135"),
    init () {
        GRAPH.submitBtn.addEventListener("click", (e) => {
            e.preventDefault()
            GRAPH.data = GRAPH.getData(GRAPH.fromDateTime.value, GRAPH.toDateTime.value)
            GRAPH.PlotGraphs(GRAPH.data)
        });
    },
    getData (from, to) {
        fetch(GRAPH.API_URL + GRAPH.clusterID, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body : JSON.stringify({
                "from": from,
                "to": to,
            })
        }).then(response => response.json()).then(data => {
            return data
        })
    },
    PlotGraphs (data=GRAPH.data) {
    }
}

document.addEventListener("DOMContentLoaded", GRAPH.init)