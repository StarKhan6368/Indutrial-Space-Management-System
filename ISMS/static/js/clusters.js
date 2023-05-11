const CLUS = {
    CLUSTERSAPI : "/api/clusters",
    clusters: [],
    clusterList : document.getElementById("cluster-list"),
    async init () {
        CLUS.clusters = await CLUS.getClusters();
        CLUS.addClusters()
    },
    addClusters () {
        CLUS.clusterList.innerHTML = "";
        CLUS.clusters.forEach(cluster => {
            let color = cluster.status === "ONLINE" ? "green" : "red";
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
            <a href="/dashboard/${cluster.id}"
                class="text-center py-2 font-bold text-white duration-500 bg-${color}-500 rounded-md md:py-3 md:px-12 hover:bg-${color}-700 hover:scale-105">Go
                to Cluster</a>
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