const EMP = {
    entriesAPI: "/api/get_entries/",
    entries : [],
    tableBody: document.getElementById("table-body"),
    svgCodes : {arrowup : "M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18",
      arrowdown: "M19.5 13.5L12 21m0 0l-7.5-7.5M12 21V3"},
    paginatorDiv: document.getElementById("paginatior-div"),
    empTable : document.getElementById("emp-table"),
    tableDrop : document.getElementById("table-drop"),
    firstName : document.getElementById("first-name"),
    lastName : document.getElementById("last-name"),
    gender : document.getElementById("gender"),
    lastPunchIn : document.getElementById("last-punch-in"),
    lastPunchOut : document.getElementById("last-punch-out"),
    adminAccess : document.getElementById("admin"),
    dateCreated : document.getElementById("acc-created"),
    position : document.getElementById("position"),
    email : document.getElementById("email"),
    phone : document.getElementById("phone-number"),
    address : document.getElementById("address"),
    dateOfBirth : document.getElementById("date-of-birth"),
    empId : document.getElementById("emp-id"),
    ID: document.URL.split("/")[4],
    data :  [],
    EMPAPI : `/api/employees/${document.URL.split("/")[4]}`,
    profileUpdater(data){
        document.getElementById("first-name").innerHTML = data.first_name;
        document.getElementById("last-name").innerHTML = data.last_name;
        document.getElementById("gender").innerHTML = data.gender;
        document.getElementById("admin").innerHTML = data.is_admin;
        document.getElementById("acc-created").innerHTML = data.acc_created;
        document.getElementById("position").innerHTML = data.position;
        document.getElementById("email").innerHTML = data.email;
        document.getElementById("phone-number").innerHTML = data.phone_number;
        document.getElementById("address").innerHTML = data.address;
        document.getElementById("date-of-birth").innerHTML = data.date_of_birth;
        document.getElementById("emp-id").innerHTML = data.emp_id;
    },
    async init(){
        EMP.data = await EMP.getData()
        EMP.addListeners()
        EMP.profileUpdater(EMP.data)
        EMP.entries = await EMP.getEntries()
        EMP.renderEntries(EMP.entries)
    },
    async getData(){
        let res = await fetch(EMP.EMPAPI);
        return await res.json();
    },
    async getEntries(){
        let res = await fetch(EMP.entriesAPI + EMP.ID);
        return await res.json();
    },
    addListeners () {
        EMP.tableDrop.addEventListener("click", (e) => {
            if (e.target.lastElementChild.id === "arrow-up"){
            e.target.lastElementChild.firstElementChild.setAttribute("d", EMP.svgCodes.arrowdown)
            e.target.lastElementChild.id = "arrow-down"
            } else {
            e.target.lastElementChild.firstElementChild.setAttribute("d", EMP.svgCodes.arrowup)
            e.target.lastElementChild.id = "arrow-up"
            }
            EMP.empTable.classList.toggle("hidden");
            EMP.paginatorDiv.classList.toggle("hidden");
        })
    },
    renderEntries(data){
        EMP.tableBody.innerHTML = ""
        data.forEach((entry) => {
            let new_entry = `<tr class="text-right border-b border-opacity-20">
            <td class="px-3 py-2 text-left">
                <span>${entry.entry_id}</span>
            </td>
            <td class="px-3 py-2 text-left">
                <span>${entry.date_time}</span>
            </td>
            <td class="px-3 py-2">
                <span>${entry.cluster_id}</span>
            </td>
            <td class="px-3 py-3">
                <span class="text-blue-600 hover:text-blue-800"><a href="/entry/${entry.photo}">${entry.photo}</a></span>
            </td>
        </tr>`
        EMP.tableBody.innerHTML += new_entry
        })
    }
}

document.addEventListener("DOMContentLoaded", EMP.init)