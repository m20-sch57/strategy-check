from flask import render_template, flash, redirect, make_response, request, send_file
from app import app
from app.forms import LoginForm, SignUp, ProblemsetID
import structures
from storage import storage
from login import Login
from sign_up import Sign_up
import useCasesAPI
import tester
import os

def info() -> list:
    logged_in = request.cookies.get("logged_in")
    username = request.cookies.get("username")
    if logged_in == None:
        logged_in = '0'
        username = "Guest"
    return [logged_in, username]

@app.route("/")
@app.route("/home")
def home():
    title = "ST Home Page"
    return render_template('home.html', title = title, info = info())

@app.route("/problemset")
def problemset():
    title = "Problems"
    problemList = useCasesAPI.getProblemset()
    return render_template('problemset.html', problemList = problemList, title = title, info = info())

@app.route("/problemset/<strId>", methods = ["GET", "POST"])
def problemset_id(strId):
    form = ProblemsetID()
    try:
        probId = int(strId)
    except ValueError:
        return redirect('/home')
    problem = storage.getProblem(probId)
    if (problem is None):
        return redirect('/home')

    username = info()[1]
    if username == "Guest":
        subList = []
    else:
        user = storage.getUserByName(username)
        subList = useCasesAPI.getSubmissionsUP(user.id, probId)

    tester.loadProblemDownloads(problem)

    paths = [path[0] for path in problem.rules.downloads]
    #paths - список путей до файлов, которые пользователь может скачать
    #print(paths)

    return render_template('problem.html.j2', form = form, title = problem.rules.name, problem = problem,
        subList = subList, info = info(), paths = paths)

@app.route("/download/app/<d1>/<d2>/<filename>")
def download(d1, d2, filename):
    #TODO if no file redirect home
    path = d1 + "/" + d2 + "/" + filename
    return send_file(path, as_attachment = True)

@app.route("/settings")
def settings():
    return render_template('settings.html', title = "Settings", info = info())

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    success, message, username = Login(form)
    flash(message)
    if success:
        resp = make_response(redirect('/home'))
        resp.set_cookie("logged_in", '1')
        resp.set_cookie("username", username)
        return resp
    return render_template('login.html', title = "Sign In", form = form, info = info())

@app.route("/logout")
def logout():
    resp = make_response(redirect("/home"))
    resp.set_cookie("logged_in", "0")
    resp.set_cookie("username", "Guest")
    return resp

@app.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    form = SignUp()
    success, message = Sign_up(form)
    flash(message)
    if success:
        return redirect("home")
    return render_template('sign_up.html', title = "Sign Up", form = form, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    title = "Code #" + subId
    return render_template('source.html.j2', title = title, id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info())

@app.route("/submissions")
def submissions():
    username = info()[1]
    if username == "Guest":
        return "..."
    user = storage.getUserByName(username)
    
    lst = useCasesAPI.getSubmissionsU(user.id)
    return render_template('submissions.html', title = "Submissions", info = info(), subList = lst)

#__________________________________
#for admin
#__________________________________

@app.route("/add_user")
def add_user():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_user.html', title = "Add user", info = info())

@app.route("/add_problem")
def add_problem():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('add_problem.html', title = "Add problem", info = info())

@app.route("/users_list")
def users_list():
    if request.cookies.get("username") != "root":
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('users_list.html', title = "Users list", info = info())

"""@app.route("/edit_user/id_user")
def edit_user():
    return None"""

"""@app.route("/edit_problem/id_problem")
def edit_problem():
    return None"""
