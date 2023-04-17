from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from forms import LoginForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "<SECRET_KEY>"

@app.route("/login", methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for("index"))
    return render_template("login.html", form=login_form)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True) 