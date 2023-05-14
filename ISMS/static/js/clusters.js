const CLUS = {
    isAdmin: false,
    CLUSTERSAPI : "/api/clusters",
    clusters: [],
    clusterList : document.getElementById("cluster-list"),
    async init () {
        data = await CLUS.getClusters();
        CLUS.isAdmin = data["is_admin"]
        CLUS.clusters = data["clusters"]
        CLUS.addClusters()
    },
    addClusters () {
        CLUS.clusterList.innerHTML = "";
        CLUS.clusters.forEach(cluster => {
            let cluster_color = cluster.status === "ONLINE" ? "green" : "red";
            let camera_color = cluster.camera_status === "ONLINE" ? "green" : "red";
            let htmlData =`<li
            class="flex flex-col justify-between p-3 space-y-3 duration-500 bg-blue-100 border-2 shadow-lg md:items-center md:flex-row rounded-xl md:space-y-0">
            <div class="flex flex-col font-semibold md:text-lg md:flex-row md:space-x-20">
                <div>
                    <h2>Cluster Name: <span class="font-normal" id="cluster-name">${cluster.name}</span>
                    </h2>
                    <p>Cluster ID: <span class="font-normal" id="cluster-id">${cluster.id}</span></p>
                </div>
                <div>
                    <p>Cluster Location: <span class="font-normal" id="cluster-location">${cluster.location}</span></p>
                    <p>Cluster Status: <span class="font-normal" id="cluster-status">${cluster.status}</span></p>
                </div>
            </div>
            <div class="flex flex-col md:space-x-2 md:flex-row space-y-2 md:space-y-0">
            <a href="/clusters/${cluster.id}"
                class="text-center py-2 font-bold text-white duration-500 bg-${cluster_color}-500 rounded-md md:py-3 md:px-12 hover:bg-${cluster_color}-700 hover:scale-105">Go
                to Cluster</a>
            ${CLUS.isAdmin ? `<a href="${cluster.camera_status === "ONLINE" ? `http://${cluster.camera}`: '#'}" 
                class="text-center py-2 font-bold text-white duration-500 bg-${camera_color}-500 rounded-md md:py-3 md:px-12 hover:bg-${camera_color}-700 hover:scale-105"
                disabled>Go to Camera</a>` : ""}
            </div>
            </li>`
            CLUS.clusterList.innerHTML += htmlData;
        })
    },
    async getClusters() {
        let res = await fetch(CLUS.CLUSTERSAPI)
        return await res.json()
    }
}

document.addEventListener("DOMContentLoaded", CLUS.init)