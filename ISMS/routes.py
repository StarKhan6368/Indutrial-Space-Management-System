from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from ISMS import app, db, bcrypt
from ISMS.forms import LoginForm, SignupForm
from ISMS.models import Users


@app.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if not current_user.is_authenticated:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            check_user = Users.query.filter_by(email_id=login_form.email_id.data).first()
            if check_user and bcrypt.check_password_hash(check_user.password, login_form.password.data):
                login_user(check_user, remember=login_form.remember_me.data)
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password", "danger")
        return render_template("login.html", form=login_form)
    return redirect(url_for("index"))

@app.route("/signup", methods=["GET","POST"])
def signup():
    if not current_user.is_authenticated:
        signup_form = SignupForm()
        if signup_form.validate_on_submit():
            user = Users.query.filter_by(email_id=signup_form.email_id.data).first()
            if not user:
                hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode("utf-8")
                new_user = Users(emp_id=signup_form.emp_id.data, email_id=signup_form.email_id.data, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                redirect(url_for('index'))
            else:
                flash("User with this Email already exists", "danger")
        return render_template("signup.html", form=signup_form)
    return redirect(url_for('index'))

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))