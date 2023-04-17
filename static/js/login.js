const APP = {
  showPassword: document.getElementById("show-password"),
  passwordInput: document.getElementById("login-password"),
  addListeners() {
    APP.showPassword.addEventListener("click", function (e) {
      APP.passwordInput.type = APP.passwordInput.type === "password" ? "text" : "password";
    });
  },
};

document.addEventListener("DOMContentLoaded", APP.addListeners);
