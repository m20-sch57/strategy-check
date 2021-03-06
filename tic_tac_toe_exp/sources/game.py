from server.gameStuff import *
from server.commonFunctions import problemFolder
from app import app
from flask import render_template
from copy import deepcopy
import os.path

FieldSize = 3
MaxScore = 100
TimeLimit = 1
TurnLimit = 100

class GameState:
    def __init__(self):
        self.a = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

    def toString(self) -> str:
        a = list(self.a[0] + self.a[1] + self.a[2])
        return ' '.join(a)

    def fromString(self, s: str) -> None:
        a = s.split()
        self.a = [a[0:3], a[3:6], a[6:9]]
        return None

class Turn:
    def __init__(self, r=0, c=0):
        self.r, self.c = r, c

    def toString(self) -> str:
        return str(self.r) + ' ' + str(self.c)

    def fromString(self, s: str) -> None:
        self.r, self.c = map(int, s.split())
        return None

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
            logPath = os.path.join('problems', problemFolder(probId), 'logs.html.j2')
            data = render_template(logPath, fieldLog = self.fieldLog,
                res1 = self.results[0].goodStr(), res2 = self.results[1].goodStr(),
                problemFolder = problemFolder(probId), **baseParams
            )
        return data

def gameStateRep(full: FullGameState, playerId: int) -> GameState:
    result = GameState()
    result.a = full.a
    return result

def lineCheck(arr, x0, y0, dx, dy):
    res = arr[x0][y0]
    for i in range(FieldSize - 1):
        if (arr[x0 + dx][y0 + dy] != arr[x0][y0]):
            return '.'
        x0 += dx
        y0 += dy
    return res

def check(full: FullGameState):
    winner = '.'
    for i in range(FieldSize):
        winner = lineCheck(full.a, i, 0, 0, 1)
        if (winner != '.'):
            return winner

    for i in range(FieldSize):
        winner = lineCheck(full.a, 0, i, 1, 0)
        if (winner != '.'):
            return winner

    winner = lineCheck(full.a, 0, 0, 1, 1)
    if (winner != '.'):
        return winner

    winner = lineCheck(full.a, 0, FieldSize - 1, 1, -1)
    if (winner != '.'):
        return winner

    return '.'

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
