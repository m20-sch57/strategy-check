from flask import render_template, flash, redirect, make_response, request
from app import app
from app.forms import LoginForm, SignUp, Submit
import demoAPI, demoAPI

@app.route("/")
@app.route("/home")
def home():
    title = "ST Home Page"
    return render_template('home.html', title = title)

@app.route("/problemset")
def problemset():
    title = "ST Problems"
    problems = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
    return render_template('problemset.html', problems = problems, title = title)

@app.route("/problemset/A")
def problemset_A():
    return render_template('problemset.html')

@app.route("/settings")
def settings():
    return render_template('settings.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        flash('Login requested for user {}, remember_me = {}'.format(form.username.data, form.remember_me.data))
        return redirect('/home')
    return render_template('login.html', title = "Sign In", form = form)

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/sign_up")
def sign_up():
    form = SignUp()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(form.username.data, form.remember_me.data))
        return redirect('/home')
    return render_template('sign_up.html', title = "Sign Up", form = form)

@app.route("/test")
def showTestPage():
    id1 = request.args.get('id1')
    id2 = request.args.get('id2')
    if (id1 == None or id2 == None):
        return "..."

    res = ''

    invocationResult = demoAPI.judge(id1, id2)
    res += invocationResult.logs.show()

    return res

@app.route("/source")
def showSource():
    id = request.args.get('id')
    if (id == None):
        return "..."

    return render_template('source.html.j2', id = id, code = demoAPI.getStrategyCode(id))

    """TODO return!!!!"""

"""#??? and other like /problem/"id_problem"/statement, submit, submissions
t = 9083927398
@app.route("/problem/" + t + "/statement")#???
def statement():
    return None"""

@app.route("/submissions")
def submissions():
    return render_template('submissions.html')

@app.route("/submit")
def submit():
    form = Submit()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me = {}'.format(form.username.data, form.remember_me.data))
        return redirect('/home')
    return render_template('submit.html', title = "Send a task", form = form)

#__________________________________
#for admin
#__________________________________

@app.route("/add_user")
def add_user():
    return render_template('add_user.html')

@app.route("/add_problem")
def add_problem():
    return render_template('add_problem.html')

@app.route("/users_list")
def users_list():
    return render_template('users_list.html')

"""@app.route("/edit_user/id_user")
def edit_user():
    return None"""

"""@app.route("/edit_problem/id_problem")
def edit_problem():
    return None"""
