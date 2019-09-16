from server.gameStuff import StrategyVerdict
from server.gameStuff import TurnState
from server.gameStuff import Result
from server.gameStuff import InvocationResult
import sys
import os
import importlib

import subprocess

shellRoute = "shell.py"
runRoute = "server/scripts/run.sh"
initRoute = "server/scripts/init.sh"

def runStrategy(game, gameModule, gameState, playerId: int, strategyModule):
    print("------------------------")
    print("turn of", playerId)
    partialGameState = game.gameStateRep(gameState, playerId)
    result = [StrategyVerdict.Ok]
    probFolder = getProbFolder(gameModule)
    strategyName = getSubmissionName(strategyModule) + ".py"
    process = subprocess.Popen(["bash", runRoute, probFolder, strategyName, str(game.TimeLimit)], bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    inp = '\n'.join([strategyModule, gameModule, partialGameState.toString(), str(playerId)])
    """
        gameState must have method toString that converts object to string WITHOUT '\n' and fromString that converts string without '\n' to object.
        turn --- the same
    """
    try:
        out, err = process.communicate(input=inp, timeout=game.TimeLimit+1000) #TODO better
    except subprocess.TimeoutExpired:
        process.kill()
        out, err = process.communicate()
        result[0] = StrategyVerdict.TimeLimitExceeded # Do not work correctly
        return result
    if 128 - process.returncode < 0:
        print("Ret code:", process.returncode)
        return [StrategyVerdict.TimeLimitExceeded]
    if process.returncode != 0:
        print("Ret code:", process.returncode)
        print(out)
        print(err)
        return [StrategyVerdict.Failed]
    turn = game.Turn()
    print("Out:", out)
    print("Err:", err)
    try:
        turn.fromString(out)
    except:
        result[0] = StrategyVerdict.PresentationError
        return result
    result.append(turn)
    return result

PlayesCount = 2

def strategyFailResults(game, strategyId : int, verdict) -> list:
    results = [Result() for i in range(PlayesCount)]
    for i in range(len(results)):
        results[i].score = game.MaxScore
    results[strategyId].score = 0
    results[strategyId].verdict = verdict
    return results

def updateLogs(logs, results):
    if (logs is not None):
        logs.processResults(results)

def endJudge(logs, results):
    updateLogs(logs, results)

def getSubmissionName(strategyModule: str) -> str:
    sPath = strategyModule.split('.')
    return sPath[-1] #TODO better than this

def getProbFolder(ModulePath: str) -> str:
    sPath = ModulePath.split('.')
    return sPath[1] #TODO better than this

def run(gameModule, classesModule, strategyModules, saveLogs = False):
    print(gameModule)
    print(strategyModules)
    game = importlib.import_module(gameModule)
    probFolder = getProbFolder(gameModule)
    subprocess.run(["bash", initRoute, probFolder])
    result = InvocationResult()
    logs = None
    if (saveLogs):
        logs = game.Logs()
        result.logs = logs
    fullGameState = game.FullGameState()
    whoseTurn = 0
    for i in range(game.TurnLimit):
        turnList = runStrategy(game, classesModule, fullGameState, whoseTurn, strategyModules[whoseTurn])
        if (turnList[0] != StrategyVerdict.Ok):
            result.results = strategyFailResults(game, whoseTurn, turnList[0])
            endJudge(logs, result.results)
            return result
        turnResult = game.makeTurn(fullGameState, whoseTurn, turnList[1], logs)
        if (turnResult[0] == TurnState.Incorrect):
            result.results = strategyFailResults(game, whoseTurn, StrategyVerdict.IncorrectTurn)
            endJudge(logs, result.results)
            return result
        if (turnResult[0] == TurnState.Last):
            result.results = turnResult[1]
            endJudge(logs, result.results)
            return result
        fullGameState = turnResult[1]
        whoseTurn = turnResult[2]
    result.results = [Result() for i in range(PlayesCount)]
    endJudge(logs, result.results)
    return result

