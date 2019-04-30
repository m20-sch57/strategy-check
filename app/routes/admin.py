from app.forRoutes.info import info, isAdmin
from flask import render_template, redirect, flash, request
from app import app
from app.forms import TournamentForm, AddProblemForm
from app.forRoutes.tournament import Tournament
from app.forRoutes.addProblem import AddProblem
import server.useCasesAPI as useCasesAPI
from app.forRoutes.changeType import changeType

@app.route("/add_user")
def add_user():
    if not isAdmin():
        flash("You don't have permission to do this!", 'message red')
        return redirect("/home")
    return render_template('add_user.html.j2', title = "Add user", info = info())

@app.route("/add_problem", methods = ["GET", "POST"])
def add_problem():
    if not isAdmin():
        flash("You don't have permission to do this!", 'message red')
        return redirect("/home")
    form = AddProblemForm()
    success, message = AddProblem(form)
    flash(message[0], message[1])
    if success:
        return redirect("/home")
    return render_template('add_problem.html.j2', title = "Add problem", form = form, info = info())


'''
@app.route("/users_list")
def users_list():
    if not isAdmin():
        flash("You don't have permission to do this!")
        return redirect("/home")
    return render_template('users_list.html.j2', title = "Users list", info = info())
'''


@app.route("/add_tournament", methods = ["GET", "POST"])
def add_tournament():
    Info = info()
    if (not Info['admin']):
        flash("You don't have permission to do this!", 'message red')
        return redirect("/home")

    default = request.args.get('probId')
    if (default == None):
        default = ''

    form = TournamentForm()
    success, message = Tournament(form)
    flash(message[0], message[1])
    if success:
        return redirect("/home")
    return render_template("add_tournament.html.j2", title = "Add tournament", form = form,
        default = default, info = Info)

@app.route("/users_list")
def usersList():
    Info = info()
    if (not isAdmin()):
        flash("You don't have permission to do this!", 'message red')
        return redirect("/home")
    message = changeType(request)
    if message != None:
        flash(message[0], message[1])
    lst = useCasesAPI.getAllUsers()
    return render_template("users_list.html.j2", title = "List of users", info = Info, lst = lst)

