from flask import render_template, redirect, url_for, flash
from flask_login import login_user

from app.auth import auth
from app.auth.forms import LoginForm
from app.models.user import User


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            username=form.username.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            return redirect(url_for("main.dashboard"))

        flash("Invalid Username or Password", "danger")

    return render_template("login.html", form=form)