const APP = {
    showPass : document.getElementById("show-pass"),
    password : document.getElementById("password"),
    confirmPassword : document.getElementById("confirm-password"),
    dismissBtn : document.querySelectorAll("#dismiss"),
    addListeners() {
        APP.showPass.addEventListener("click", () => {
            if (APP.password.type === "password") {
                APP.password.type = "text";
                APP.confirmPassword.type = "text";
                APP.showPass.classList.add("fa-eye-slash");
                APP.showPass.classList.remove("fa-eye");
            } else {
                APP.password.type = "password";
                APP.confirmPassword.type = "password";
                APP.showPass.classList.add("fa-eye");
                APP.showPass.classList.remove("fa-eye-slash");
            }
        });
        if(APP.dismissBtn.length !== 0) {
            APP.dismissBtn.forEach((btn) => {
                btn.addEventListener("click", () => {
                    btn.parentElement.parentElement.remove()
                })
            })
        }
    }
}

window.addEventListener("DOMContentLoaded", APP.addListeners);