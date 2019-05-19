from classes import *
from server.gameStuff import *
from app import app
from flask import render_template
from copy import deepcopy
import os.path
from module import check
from module import lineCheck
from module import FieldSize

MaxScore = 100
TimeLimit = 1
TurnLimit = 100

class FullGameState:
    def __init__(self):
        self.a = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

class Logs:
    def __init__(self):
        self.fieldLog = []

    def processResults(self, results):
        self.results = results

    def update(self, a, turn):
        b = [[['.', 0] for i in range(FieldSize)] for i in range(FieldSize)]
        for i in range(FieldSize):
            for j in range(FieldSize):
                b[i][j] = [a[i][j], 0]
                if (turn.r == i and turn.c == j):
                    b[i][j][1] = 1
        self.fieldLog.append(b)

    def show(self, probId, baseParams):
        with app.app_context():
            logPath = os.path.join('problems', str(probId), 'logs.html.j2')
            data = render_template(logPath, fieldLog = self.fieldLog,
                res1 = self.results[0].goodStr(), res2 = self.results[1].goodStr(),
                strId = str(probId), **baseParams
            )
        return data

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.a = full.a
    return result





def makeTurn(gameState: FullGameState, playerId: int, turn: Turn, logs = None) -> list:
    charList = ['X', 'O']
    if (turn.r < 0 or turn.r >= FieldSize or turn.c < 0 or turn.c >= FieldSize or gameState.a[turn.r][turn.c] != '.'):
        return [TurnState.Incorrect, gameState, nextPlayer(playerId)]
    gameState.a[turn.r][turn.c] = charList[playerId]
    if (logs is not None):
        logs.update(gameState.a, turn)
    winner = check(gameState)
    if (winner == '.'):
        dot = 0
        for i in gameState.a:
            for j in i:
                if (j == '.'):
                    dot = 1
        if (dot == 1):
            return [TurnState.Correct, gameState, nextPlayer(playerId)]
        else:
            return [TurnState.Last, [Result(StrategyVerdict.Ok, MaxScore // 2), Result(StrategyVerdict.Ok, MaxScore // 2)]]
    else:
        if (winner == 'X'):
            return [TurnState.Last, [Result(StrategyVerdict.Ok, MaxScore), Result(StrategyVerdict.Ok, 0)]]
        else:
            return [TurnState.Last, [Result(StrategyVerdict.Ok, 0), Result(StrategyVerdict.Ok, MaxScore)]]
