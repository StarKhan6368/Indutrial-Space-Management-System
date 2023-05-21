const PLAY = {
    "filesAPI": "api/rtttl_files",
    "mqttAPI": "api/mqtt_rtttl",
    "searchInp" : document.getElementById("rtttl"),
    "rtttlList": document.getElementById("rtttl-list"),
    "fetchList": [],
    "fetchCount": 0,
    "idleInterval": 2000,
    "typingTimer":null,
    filterRtttlFiles(){
        if (PLAY.searchInp.value !== ""){
            PLAY.renderFiles(PLAY.fetchList.filter(file => file.includes(PLAY.searchInp.value)));
        } else {
            PLAY.renderFiles(PLAY.fetchList.slice(0, 50))
        }
    },
    async init() {
        await PLAY.fetchFiles();
        PLAY.renderFiles(PLAY.fetchList.slice(0, 50));
        PLAY.searchInp.addEventListener("keyup", () => {
            clearTimeout(PLAY.typingTimer)
            setTimeout(PLAY.filterRtttlFiles, PLAY.idleInterval);
        })
        PLAY.searchInp.addEventListener("keydown", () => {
            clearTimeout(PLAY.typingTimer)
        })
    },
    async fetchFiles() {
        await fetch(PLAY.filesAPI
            ).then(res => res.json()).then(data => {
                PLAY.fetchList = data["file_list"];
                PLAY.fetchCount = data["total"];
            })
    },
    renderFiles(file_list){
        PLAY.rtttlList.innerHTML = "";
        file_list.forEach(file => {
            let listElem = `<li
            class="flex flex-col items-center p-2 space-y-3 duration-500 bg-blue-100 border-2 shadow-lg rounded-xl">
                <h2 id="rtttl-name" class="text-lg font-medium">${file.slice(0, file.lastIndexOf("."))}</h2>
                <button id="play-btn"
                    class="w-full py-1 font-bold text-white duration-500 bg-green-500 rounded-md hover:bg-green-700 hover:scale-105">Play</button>
            </li>`
            PLAY.rtttlList.innerHTML += listElem;
        });
        document.querySelectorAll("#play-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.preventDefault();
                rtttlFileName = e.target.previousElementSibling.textContent
                fetch(PLAY.mqttAPI, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "file_name": rtttlFileName
                    })
                })
            })    
        })
    }

}
document.addEventListener("DOMContentLoaded", PLAY.init)