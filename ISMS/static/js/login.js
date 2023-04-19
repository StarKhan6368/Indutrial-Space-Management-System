const APP = {
    showPassBtn : document.getElementById("show-pass"),
    loginPass: document.getElementById("login-password"),
    emailId: document.getElementById("login-email"),
    addListeners () {
        APP.showPassBtn.addEventListener("click", (e) => {
            if (APP.showPassBtn.classList.contains("fa-eye")) {
                APP.showPassBtn.classList.remove("fa-eye");
                APP.showPassBtn.classList.add("fa-eye-slash");
                APP.loginPass.type = "text";
            } else {
                APP.showPassBtn.classList.remove("fa-eye-slash");
                APP.showPassBtn.classList.add("fa-eye");
                APP.loginPass.type = "password";
            }
        });
    },
}

document.addEventListener("DOMContentLoaded", APP.addListeners)