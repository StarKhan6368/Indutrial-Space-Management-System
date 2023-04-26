const APP = {
    sideNav : document.getElementById("sidebar-nav"),
    logo : document.getElementById("logo"),
    addListeners () {
        APP.logo.addEventListener("click", () => {
          APP.sideNav.classList.toggle("hidden");
        });
        APP.highlightIcon();
    },
    highlightIcon () {
      currentWindow = document.URL.split("/")[3];
      if (currentWindow === "" || currentWindow === "/") {
        currentWindow = "home";
      }
      currentIcon = document.getElementById(currentWindow);
      currentIcon.classList.add("bg-white");
      currentIcon.firstElementChild.firstElementChild.classList.remove("stroke-white");
      currentIcon.firstElementChild.firstElementChild.classList.add("stroke-gray-800");
    }
}

document.addEventListener("DOMContentLoaded", APP.addListeners)