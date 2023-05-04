const PLOTTER = {
    clusterID: document.URL.split("/")[4],
    latestAPI : "/api/latest/",
    thresholdAPI : "/api/thresholds",
    status : document.getElementById("status"),
    date_time : document.getElementById("date_time"),
    cluster_id : document.getElementById("cluster_id"),
    temperature : document.getElementById("temperature"),
    free_heap: document.getElementById("free_heap"),
    humidity : document.getElementById("humidity"),
    pressure : document.getElementById("pressure"),
    lpg : document.getElementById("lpg"),
    methane : document.getElementById("methane"),
    smoke : document.getElementById("smoke"),
    hydrogen: document.getElementById("hydrogen"),
    ppm : document.getElementById("ppm"),
    thresholds : {},
    colorChanger(param, exceed){
        let from = "red";
        let to = "green";
        if (exceed) {
            from = "green";
            to = "red";
        }
        param.parentElement.className = param.parentElement.className.replaceAll(from, to);
    },
    colorCoder() {
        for (const param in PLOTTER.thresholds) {
            if (PLOTTER[param].childNodes[0].textContent >= PLOTTER.thresholds[param]) {
                PLOTTER.colorChanger(PLOTTER[param], true);
            } else {
                PLOTTER.colorChanger(PLOTTER[param], false);
            }
        PLOTTER.colorChanger(PLOTTER.status, PLOTTER.status === "OFFLINE");
        }
    },
    async init () {
        PLOTTER.thresholds = await fetch(PLOTTER.thresholdAPI).then(response => response.json()).then(data => {return data;})
        PLOTTER.parameterUpdater()
        // intervalId = setInterval(PLOTTER.parameterUpdater, 5000);
    },
    async parameterUpdater() {
        await fetch(PLOTTER.latestAPI+PLOTTER.clusterID).then(response => response.json()).then(data => {
            for (const param in data) {
                PLOTTER[param].childNodes[0].textContent = data[param];            
            }
        })
        return PLOTTER.colorCoder()
    }
}

document.addEventListener("DOMContentLoaded", PLOTTER.init);