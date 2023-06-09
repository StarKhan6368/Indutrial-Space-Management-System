from flask import Blueprint, redirect, url_for, render_template, flash
from ISMS import bcrypt, db
from flask_login import current_user, login_user, logout_user
from ISMS.users.forms import LoginForm, SignupForm
from ISMS.models import User, Employee
users = Blueprint("users", __name__)

@users.route("/login", methods=["GET","POST"])
def login():
    if not current_user.is_authenticated:
        login_form = LoginForm()
        if login_form.validate_on_submit():
            check_user = User.query.filter_by(email_id=login_form.email_id.data).first()
            if check_user and bcrypt.check_password_hash(check_user.password, login_form.password.data) and check_user.status != "PENDING":
                login_user(check_user, remember=login_form.remember_me.data)
                current_user.status = "ONLINE"
                db.session.commit()
                return redirect(url_for('main.index'))
            elif check_user and check_user.status == "PENDING":
                flash("Account is not activated, Await Admin Confirmation", "warning")
            else:
                flash("Invalid email or password", "danger")
        return render_template("login.html", form=login_form)
    return redirect(url_for("main.index"))

@users.route("/signup", methods=["GET","POST"])
def signup():
    if not current_user.is_authenticated:
        signup_form = SignupForm()
        if signup_form.validate_on_submit():
            user = User.query.filter_by(emp_id=signup_form.emp_id.data).first()
            employee = Employee.query.filter_by(emp_id=signup_form.emp_id.data.lower()).first()
            if not user and employee:
                email_check = User.query.filter_by(email_id=signup_form.email_id.data).first()
                if email_check:
                    flash("Email already exists", "danger")
                    return render_template("signup.html", form=signup_form)
                hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode("utf-8")
                new_user = User(emp_id=signup_form.emp_id.data.lower(), email_id=signup_form.email_id.data, password=hashed_password, status="PENDING", is_admin=False)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('users.login'))
            elif not employee:
                flash("Invalid Employee ID", "danger")
            else:
                flash("Account with Employee ID already exists", "danger")
        return render_template("signup.html", form=signup_form)
    return redirect(url_for('main.index'))

@users.route("/logout")
def logout():
    if current_user.is_authenticated:
        current_user.status = "OFFLINE"
        db.session.commit()
        logout_user()
    return redirect(url_for('users.login'))

@users.route("/profile")
def profile():
    return "HELLO"
        