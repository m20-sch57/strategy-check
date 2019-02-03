from structures import ProblemState, StrategyState, UserType
from structures import User, Rules, Problem, Submission, Tournament
from commonFunctions import readFile
import os

os.remove('database.db')

from storage import storage
import useCasesAPI

StrategyCnt = 10

game = readFile("tic_tac_toe/game.py")
classes = readFile("tic_tac_toe/classes.py")
logsTemplate = readFile("tic_tac_toe/templates/logs.html.j2")
css = readFile("tic_tac_toe/static/style.css")

sources = [
    ['problems/0/game.py', game], 
    ['problems/0/classes.py', classes], 
    ['app/templates/problems/0/logs.html.j2', logsTemplate],
    ['app/static/problems/0/style.css', css]
]

downloads = [
	['app/downloads/0/classes.py', classes]
]

statement = readFile("Text/trashST")

rules = Rules("TicTacToe", sources, downloads, statement)
subs = [i for i in range(10)]

TicTacToe = Problem(-1, rules, set(subs), [])

storage.saveProblem(TicTacToe)

for i in range(StrategyCnt):
    user = User(-1, "hlebushek" + str(i), "12345", UserType.Default, {0 : [i]})
    storage.saveUser(user)

for i in range(StrategyCnt):
    sub = Submission(-1, i, 0, readFile("tic_tac_toe/strategies/st" + str(i + 1) + ".py"), StrategyState.Main)
    storage.saveSubmission(sub)

useCasesAPI.addUser("test", "123")
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st1.py"))
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st2.py"))
useCasesAPI.addSubmission(10, 0, readFile("tic_tac_toe/strategies/st3.py"))
