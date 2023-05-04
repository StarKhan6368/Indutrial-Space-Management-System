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
  
  document.addEventListener("DOMContentLoaded", DASH.addListeners)