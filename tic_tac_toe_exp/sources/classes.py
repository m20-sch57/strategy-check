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

