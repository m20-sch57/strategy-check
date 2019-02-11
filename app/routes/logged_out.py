from flask import render_template, make_response, redirect, flash
from app import app
from app.forRoutes.info import info
from app.forms import LoginForm, SignUp
from app.forRoutes.login import Login
from app.forRoutes.sign_up import Sign_up

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    success, message, username, userId = Login(form)
    flash(message)
    if success:
        resp = make_response(redirect('/home'))
        resp.set_cookie("logged_in", '1')
        resp.set_cookie("username", username)
        resp.set_cookie("user_id", userId)
        return resp
    return render_template('login.html', title = "Sign In", form = form, info = info())

@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    form = SignUp()
    success, message = Sign_up(form)
    flash(message)
    if success:
        return redirect("home")
    return render_template('sign_up.html', title = "Sign Up", form = form, info = info())
