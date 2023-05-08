const LATEST = {
  clusterID: document.URL.split("/")[4],
  latestAPI : `/api/clusters/CLUSTER_ID/latest`,
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
      for (const param in LATEST.thresholds) {
          if (LATEST[param].childNodes[0].textContent >= LATEST.thresholds[param]) {
              LATEST.colorChanger(LATEST[param], true);
          } else {
              LATEST.colorChanger(LATEST[param], false);
          }
      LATEST.colorChanger(LATEST.status, LATEST.status.textContent === "OFFLINE");
      LATEST.colorChanger(LATEST.free_heap, LATEST.free_heap <= LATEST.thresholds["free_heap"]);
      }
  },
  async init () {
      LATEST.thresholds = await fetch(LATEST.thresholdAPI).then(response => response.json()).then(data => {return data;})
      LATEST.parameterUpdater()
      intervalId = setInterval(LATEST.parameterUpdater, 5000);
  },
  async parameterUpdater() {
      await fetch(LATEST.latestAPI.replace("CLUSTER_ID", LATEST.clusterID)).then(response => response.json()).then(data => {
          for (const param in data) {
              LATEST[param].childNodes[0].textContent = data[param];            
          }
      })
      return LATEST.colorCoder()
  }
}

const DASH = {
  svgCodes : {arrowup : "M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18",
    arrowdown: "M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"},
  latestPara : document.getElementById("latest-parameters"),
  latestParaDrop : document.getElementById("latest-parameters-dropdown"),
  chartPara : document.getElementById("chart-parameters"),
  chartParaDrop : document.getElementById("chart-parameters-dropdown"),
  addListeners () {
    DASH.latestParaDrop.addEventListener("click", (e) => {
      if (e.target.lastElementChild.id === "arrow-up"){
        e.target.lastElementChild.firstElementChild.setAttribute("d", DASH.svgCodes.arrowdown)
        e.target.lastElementChild.id = "arrow-down"
      } else {
        e.target.lastElementChild.firstElementChild.setAttribute("d", DASH.svgCodes.arrowup)
        e.target.lastElementChild.id = "arrow-up"
      }
      DASH.latestPara.classList.toggle("hidden");
    })
    DASH.chartParaDrop.addEventListener("click", (e) => {
      if (e.target.lastElementChild.id === "arrow-up"){
        e.target.lastElementChild.firstElementChild.setAttribute("d", DASH.svgCodes.arrowdown)
        e.target.lastElementChild.id = "arrow-down"
      } else {
        e.target.lastElementChild.firstElementChild.setAttribute("d", DASH.svgCodes.arrowup)
        e.target.lastElementChild.id = "arrow-up"
      }
      DASH.chartPara.classList.toggle("hidden");
    })
  }
}

document.addEventListener("DOMContentLoaded", () => {LATEST.init(); DASH.addListeners()});