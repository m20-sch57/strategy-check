from server.structures import ProblemState, StrategyState, UserType
from server.structures import User, Rules, Problem, Submission, Tournament
from server.storage import storage
from server.gameStuff import StrategyVerdict, Result, InvocationResult
from server.commonFunctions import printToFile, unixTime, problemFolder
import os
import server.judge as judge
import sys

#TODO: same name of modules

def loadSources(sources, problems=False):
    for source in sources:
        path = source[0]
        printToFile(source[1], path)
        if (problems):
            pathParts = path.split('/')
            if (pathParts[0] == "problems" and pathParts[2] == "classes.py"): #TODO better
                printToFile(source[1], "/home/test/" + path) #TODO better

def loadProblem(problem):
    loadSources(problem.rules.sources, True)

def loadProblemDownloads(problem):
    loadSources(problem.rules.downloads)

def getName(submission):
    return "sub" + str(submission.id)

def getStrategyModule(submission):
    return '.'.join(['problems', problemFolder(submission.probId),
        'strategies', getName(submission)])

def getFilename(submission):
    return getName(submission) + ".py"

def loadSubmission(submission, problem):
    for prefix in [["."], ["/home", "test"]]: #TODO "test" -> username, '/' -> os.sep
        filename = os.path.join(*prefix, 'problems', problemFolder(problem.id),
            'strategies', getFilename(submission))
        print(filename)
        printToFile(submission.code, filename)

def getGameModule(problem):
    return '.'.join(['problems', problemFolder(problem.id), 'game'])

def getClassesModule(problem):
    return '.'.join(["problems", problemFolder(problem.id), "classes"])

def testStrategies(id1, id2, saveLogs = False):
    sub1 = storage.getSubmission(id1)
    sub2 = storage.getSubmission(id2)

    if (sub1.probId != sub2.probId):
        raise Exception('Trying to judge two strategies for different problems')

    problemId = sub1.probId
    problem = storage.getProblem(problemId)
    loadProblem(problem)

    loadSubmission(sub1, problem)
    loadSubmission(sub2, problem)

    invocationResult = judge.run(
        getGameModule(problem),
        getClassesModule(problem),
        [getStrategyModule(sub1), getStrategyModule(sub2)],
        saveLogs = saveLogs
    )
    return invocationResult

def tournament(problemId):
    problem = storage.getProblem(problemId)
    problem.type = ProblemState.Testing
    storage.saveProblem(problem)
    loadProblem(problem)

    subCnt = len(problem.submissions)
    subs = [storage.getSubmission(subId) for subId in problem.submissions]
    scores = [[0, subs[i].id] for i in range(subCnt)]

    for i in range(subCnt):
        loadSubmission(subs[i], problem)

    problemPath = os.path.join('problems', str(problemId))

    for i in range(subCnt):
        for j in range(subCnt):
            if (i != j):
                print("judging ", i, j)
                invocationResult = judge.run(
                    getGameModule(problem),
                    getClassesModule(problem),
                    [getStrategyModule(subs[i]), getStrategyModule(subs[j])],
                    saveLogs = False
                )
                print(invocationResult.results[0].goodStr())
                print(invocationResult.results[1].goodStr())
                scores[i][0] += invocationResult.results[0].score
                scores[j][0] += invocationResult.results[1].score

    scores.sort(reverse = True)
    newTournament = Tournament(-1, problemId, problem.revisionId, unixTime(), scores)
    newTournamentId = storage.saveTournament(newTournament)
    problem.tournaments.append(newTournamentId)
    storage.saveProblem(problem)
    return newTournamentId
