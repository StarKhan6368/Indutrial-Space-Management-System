const USERS = {
    empList : document.getElementById("emp-list"),
    EMPLOYEESAPI : "/api/employees/filter",
    CONFIRMAPI: "/api/user/confirm",
    data:[],
    values: {status: "PENDING"},
    empSearch : document.getElementById("emp-search"),
    async init(){
        await USERS.getEMPS()
        USERS.populateEmps(USERS.data);
        USERS.empSearch.addEventListener("input", (e) => {
            let tempData = USERS.data.filter((emp)=>{
                return emp.first_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.last_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.email_id.toLowerCase().includes(e.target.value.toLowerCase()) || emp.emp_id.toLowerCase().includes(e.target.value.toLowerCase())
            })
            USERS.populateEmps(tempData);
        })
        USERS.addListeners();
    },
    addListeners() {
        confirmBtns = document.querySelectorAll("#confirm-btn");
        confirmBtns.forEach((btn) => {
            btn.addEventListener("click", (e) => {
                if (confirm("Are you sure you want to add this User? ")){
                    employee_id = e.target.previousElementSibling.firstElementChild.firstElementChild.textContent.split(":")[1];
                    console.log(employee_id);
                    fetch(USERS.CONFIRMAPI, {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"emp_id": employee_id.trim()})
                    })
                }
            })
        })
    },
    populateEmps(data){
        USERS.empList.innerHTML = "";
        data.forEach(employee => {
            color = "green"
            empCard = `<li
            class="flex flex-col justify-between p-3 space-y-3 duration-500 bg-blue-100 border-2 shadow-lg md:items-center md:flex-row rounded-xl md:space-y-0">
            <div class="flex flex-col font-semibold md:text-lg md:flex-row md:space-x-20">
                <div>
                    <p>Employee ID: <span class="font-normal" id="Employee-id">${employee.emp_id}</span></p>
                    <h2>Employee Name: <span class="font-normal" id="Employee-name">${employee.first_name + " " + employee.last_name}</span>
                    </h2>
                </div>
                <div>
                    <p>Employee Email: <span class="font-normal" id="Employee-email">${employee.email_id}</span></p>
                    <p>Employee Status: <span class="font-normal" id="Employee-status">${employee.status}</span></p>
                </div>
                <div>
                    <p>Accoount Created On: <span class="font-normal" id="Employee-id">${employee.acc_created}</span></p>
                    <p>Employee Position: <span class="font-normal" id="Employee-status">${employee.position}</span></p>
                </div>
            </div>
            <button id="confirm-btn"
                class="text-center py-2 font-bold text-white duration-500 bg-${color}-500 rounded-md md:py-3 md:px-12 hover:bg-${color}-700 hover:scale-105">Confirm User</button>
            </li>`
            USERS.empList.innerHTML += empCard;
        });
    },
    async getEMPS() {
        let res = await fetch(USERS.EMPLOYEESAPI, {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(USERS.values)
        })
        USERS.data = await res.json()
    }
}

document.addEventListener("DOMContentLoaded", USERS.init)