const EMPS = {
    empList : document.getElementById("emp-list"),
    EMPLOYEESAPI : "/api/employees",
    data:[],
    values: ["emp_id", "first_name", "last_name"],
    empSearch : document.getElementById("emp-search"),
    async init(){
        await EMPS.getEMPS()
        EMPS.populateEmps(EMPS.data);
        EMPS.empSearch.addEventListener("input", (e) => {
            let tempData = EMPS.data.filter((emp)=>{
                return emp.first_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.last_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.email.toLowerCase().includes(e.target.value.toLowerCase()) || emp.emp_id.toLowerCase().includes(e.target.value.toLowerCase())
            })
            EMPS.populateEmps(tempData);
        })
    },
    populateEmps(data){
        EMPS.empList.innerHTML = "";
        data.forEach(employee => {
            color = employee.status == "ONLINE" ? "green" : "red";
            empCard = `<li
            class="flex flex-col justify-between p-3 space-y-3 duration-500 bg-blue-100 border-2 shadow-lg md:items-center md:flex-row rounded-xl md:space-y-0">
            <div class="flex flex-col font-semibold md:text-lg md:flex-row md:space-x-20">
                <div>
                    <h2>Employee Name: <span class="font-normal" id="Employee-name">${employee.first_name + " " + employee.last_name}</span>
                    </h2>
                    <p>Employee ID: <span class="font-normal" id="Employee-id">${employee.emp_id}</span></p>
                </div>
                <div>
                    <p>Employee Email: <span class="font-normal" id="Employee-email">${employee.email}</span></p>
                    <p>Employee Status: <span class="font-normal" id="Employee-status">${employee.status || "NA"}</span>
                    </p>
                </div>
            </div>
            <a href="/employees/${employee.emp_id}"
                class="text-center py-2 font-bold text-white duration-500 bg-${color}-500 rounded-md md:py-3 md:px-12 hover:bg-${color}-700 hover:scale-105">Go
                to employee</a>
            </li>`
            EMPS.empList.innerHTML += empCard;
        });
    },
    async getEMPS() {
        let res = await fetch(EMPS.EMPLOYEESAPI, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(EMPS.values)
        })
        EMPS.data = await res.json()
    }
}

document.addEventListener("DOMContentLoaded", EMPS.init)