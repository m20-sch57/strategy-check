import json

class GameState:
    turns = [[], []]

    def toString(self):
        return str(json.dumps(self.turns))

    def fromString(self, s):
        self.turns = json.loads(s)

class Turn:
    def __init__(self, trust: int=0):
        self.trust = trust

    def toString(self):
        return str(self.trust)

    def fromString(self, s):
        self.trust = int(s)
