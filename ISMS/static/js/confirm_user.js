const USERS = {
    empList : document.getElementById("emp-list"),
    EMPLOYEESAPI : "/api/users/filter",
    CONFIRMAPI: "/api/user/confirm",
    data:[],
    values: {status: "PENDING"},
    empSearch : document.getElementById("emp-search"),
    async init(){
        await USERS.getEMPS()
        if (Object.keys(USERS.data).length !== 0) {
            USERS.populateEmps(USERS.data);
        }
        USERS.empSearch.addEventListener("input", (e) => {
            if (Object.keys(USERS.data).length !== 0) {
                let tempData = USERS.data.filter((emp)=>{
                    return emp.first_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.last_name.toLowerCase().includes(e.target.value.toLowerCase()) || emp.email_id.toLowerCase().includes(e.target.value.toLowerCase()) || emp.emp_id.toLowerCase().includes(e.target.value.toLowerCase())
                })
                USERS.populateEmps(tempData);
            }
        })
        USERS.addListeners();
    },
    addListeners() {
        confirmBtnsUser = document.querySelectorAll("#confirm-btn-user");
        confirmBtnAdmin = document.querySelectorAll("#confirm-btn-admin");
        confirmBtnsUser.forEach((btn) => {
            btn.addEventListener("click", (e) => {
                if (confirm("Are you sure you want to add this Employee as User ? ")){
                    employee_id = e.target.parentElement.previousElementSibling.firstElementChild.firstElementChild.textContent.split(":")[1];
                    fetch(USERS.CONFIRMAPI, {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"emp_id": employee_id.trim(), "is_admin":false})
                    })
                    e.target.parentElement.parentElement.remove()
                }
            })
        })
        confirmBtnAdmin.forEach((btn) => {
            btn.addEventListener("click", (e) => {
                if (confirm("Are you sure you want to add this Employee as Admin ? ")){
                    employee_id = e.target.parentElement.previousElementSibling.firstElementChild.firstElementChild.textContent.split(":")[1];
                    fetch(USERS.CONFIRMAPI, {
                        method: "POST",
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({"emp_id": employee_id.trim(), "is_admin":true})
                    })
                    e.target.parentElement.parentElement.remove()
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
                    <h2>Employee Name: <span class="font-normal" id="Employee-name">${employee.first_name + " " + employee.last_name}</span></h2>
                    <p>Employee Email: <span class="font-normal" id="Employee-email">${employee.email_id}</span></p>
                </div>
                <div>
                    <p>Employee Status: <span class="font-normal" id="Employee-status">${employee.status}</span></p>
                    <p>Accoount Created On: <span class="font-normal" id="Employee-id">${employee.acc_created}</span></p>
                    <p>Employee Position: <span class="font-normal" id="Employee-status">${employee.position}</span></p>
                </div>
            </div>
            <div class="flex md:space-x-2 flex-col md:flex-row space-y-2 md:space-y-0">
                <button id="confirm-btn-user"
                    class="text-center py-2 font-bold text-white duration-500 bg-${color}-500 rounded-md md:py-3 md:px-12 hover:bg-${color}-700 hover:scale-105">Confirm User as User</button>
                <button id="confirm-btn-admin"
                    class="text-center py-2 font-bold text-white duration-500 bg-${color}-500 rounded-md md:py-3 md:px-12 hover:bg-${color}-700 hover:scale-105">Confirm User as Admin</button>
            </div>
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