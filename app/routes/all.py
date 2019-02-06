from app.forRoutes.info import info
from flask import render_template, redirect, send_file
from app import app
from app.forRoutes.problemsetId import problemsetId
from app.forms import ProblemsetID
import server.useCasesAPI as useCasesAPI

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
    success, paths, problem, subList = problemsetId(form, strId)
    if not success:
        return redirect("/home")
#    smth with paths...
    return render_template('problem.html.j2', form = form, title = problem.rules.name, problem = problem, subList = subList, paths = paths, info = info())

@app.route("/source/<subId>")
def showSource(subId):
    title = "Code #" + subId
    return render_template('source.html.j2', id = subId, code = useCasesAPI.getSubmissionCode(subId), info = info())

@app.route("/download/app/<d1>/<d2>/<filename>")
def download(d1, d2, filename):
    #TODO if no file redirect home
    path = d1 + "/" + d2 + "/" + filename
    return send_file(path, as_attachment = True)

