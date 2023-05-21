const AEMP = {
    captureBtn : document.getElementById("btn-img"),
    encodeApi:"/api/capture_and_validate",
    cameraApi:"/api/clusters_camera/",
    cameraIp:"",
    faceEncInput:document.getElementById("face-enc-input"),
    imgFrame: document.getElementById("frame-img"),
    dismissBtn : document.querySelectorAll("#dismiss"),
    clusterId: document.getElementById("cluster-id"),
    addListeners () {
        if(AEMP.dismissBtn.length !== 0) {
            AEMP.dismissBtn.forEach((btn) => {
                btn.addEventListener("click", () => {
                    btn.parentElement.parentElement.remove()
                })
            })
        }
        AEMP.captureBtn.addEventListener("click", (e) => {
            const tempSrc = AEMP.imgFrame.src
            AEMP.imgFrame.src = `http://${AEMP.cameraIp}/capture`;
            e.preventDefault();
            fetch(AEMP.encodeApi, {
                method: "POST",
                headers:{
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({
                    camera_ip: AEMP.cameraIp
                })
            }).then(res => res.json()).then(data => {
                if (data["encoding"]) {
                    if (AEMP.captureBtn.className.includes("blue")){
                        AEMP.captureBtn.className = AEMP.captureBtn.className.replaceAll("blue", "green")
                    } else {
                        AEMP.captureBtn.className = AEMP.captureBtn.className.replaceAll("red", "green")
                    }
                    AEMP.faceEncInput.value = data["encoding"];
                } else {
                    if (AEMP.captureBtn.className.includes("blue")){
                        AEMP.captureBtn.className = AEMP.captureBtn.className.replaceAll("blue", "red")
                    } else {
                        AEMP.captureBtn.className = AEMP.captureBtn.className.replaceAll("green", "red")
                    }
                    AEMP.imgFrame.src = tempSrc
                }
            })
        })
        AEMP.clusterId.addEventListener("change", () => {
            AEMP.fetchCameraStats()
        })
        AEMP.fetchCameraStats()
    },
    fetchCameraStats() {
        fetch(AEMP.cameraApi + AEMP.clusterId.value).then(res => res.json()).then(data => {
            AEMP.imgFrame.src = "http://" + data["camera_ip"]+":81";
            AEMP.cameraIp = data["camera_ip"];

        })
    }
}

document.addEventListener("DOMContentLoaded", AEMP.addListeners)